import pyodbc
import base64
import json
import logging
import os
from datetime import datetime
from PIL import Image
import io
import requests
from typing import Dict, Any, Optional
import time

class AIProductApproval:
    def __init__(self):
        self.setup_logging()
        self.db_connection = None
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "mistral:7b"
        
    def setup_logging(self):
        """Setup logging to file"""
        log_dir = r"C:\AI_Approval_Logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"ai_approval_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Also print to console
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def connect_database(self):
        """Connect to Azure SQL Database"""
        try:
            connection_string = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=tcp:kykmarketserver.database.windows.net,1433;"
                "DATABASE=KYKMarketDb;"
                "UID=adminuser;"
                "PWD=1E*DCkf.4!d*h6;"
                "Encrypt=yes;"
                "TrustServerCertificate=no;"
                "Connection Timeout=30;"
            )
            
            self.db_connection = pyodbc.connect(connection_string)
            self.logger.info("Database connection established successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)}")
            return False
            
    def get_pending_products(self) -> list:
        """Get all pending products that need AI approval"""
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT p.ProductId, p.PName, p.PDesc, p.PPrice, p.PStock, 
                       p.PKyk, p.PImage, p.UserId, u.Name, u.Surname
                FROM Product p
                INNER JOIN Users u ON p.UserId = u.UserId
                WHERE p.PStatus = 0 AND p.RequiresManualReview IS NULL
                ORDER BY p.ProductId
            """
            
            cursor.execute(query)
            products = []
            for row in cursor.fetchall():
                products.append({
                    'ProductId': row[0],
                    'PName': row[1] or '',
                    'PDesc': row[2] or '',
                    'PPrice': row[3] or 0,
                    'PStock': row[4] or 0,
                    'PKyk': row[5] or '',
                    'PImage': row[6],
                    'UserId': row[7],
                    'SellerName': f"{row[8] or ''} {row[9] or ''}".strip()
                })
                
            self.logger.info(f"Found {len(products)} pending products")
            return products
            
        except Exception as e:
            self.logger.error(f"Error fetching pending products: {str(e)}")
            return []
            
    def process_image_for_ai(self, image_data: bytes) -> str:
        """Process image for AI analysis"""
        try:
            if not image_data:
                return "No image provided"
                
            # Convert image to base64
            image = Image.open(io.BytesIO(image_data))
            
            # Resize image to reduce processing time (max 512x512)
            image.thumbnail((512, 512), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return f"data:image/jpeg;base64,{img_base64}"
            
        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            return "Image processing failed"
            
    def create_ai_prompt(self, product: Dict[str, Any]) -> str:
        """Create prompt for AI analysis"""
        image_data = self.process_image_for_ai(product['PImage'])
        
        prompt = f"""You are an AI moderator for a student dormitory marketplace. Analyze this product and decide if it should be approved or rejected.

PRODUCT DETAILS:
- Name: {product['PName']}
- Description: {product['PDesc']}
- Price: {product['PPrice']} TL
- Stock: {product['PStock']} units
- Dormitory: {product['PKyk']}
- Seller: {product['SellerName']}
- Image: {image_data if image_data != "No image provided" else "No image available"}

APPROVAL GUIDELINES:
✅ APPROVE if:
- Product is appropriate for students (18+)
- No inappropriate content or images
- Reasonable pricing
- Clear, honest description
- Legal and acceptable items

❌ REJECT if:
- Contains 18+ content or inappropriate images
- Contains cuss words or offensive language
- Illegal items or services
- Suspicious pricing (too high/low)
- Unclear or misleading description
- Inappropriate for student environment

RESPOND IN JSON FORMAT ONLY:
{{
    "decision": "APPROVE" or "REJECT",
    "reason": "Brief explanation of decision",
    "confidence": 0.0-1.0,
    "content_analysis": "What you see in the image/text"
}}

Be strict about content moderation. When in doubt, reject for manual review."""

        return prompt
        
    def call_ollama(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Call Ollama API for AI analysis"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temperature for consistent decisions
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=60  # 60 second timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                
                # Try to parse JSON response
                try:
                    # Find JSON in response
                    start_idx = ai_response.find('{')
                    end_idx = ai_response.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx != 0:
                        json_str = ai_response[start_idx:end_idx]
                        decision = json.loads(json_str)
                        
                        # Validate decision format
                        required_fields = ['decision', 'reason', 'confidence']
                        if all(field in decision for field in required_fields):
                            return decision
                            
                except json.JSONDecodeError:
                    self.logger.warning(f"Failed to parse JSON response: {ai_response}")
                    
                # Fallback: simple text parsing
                ai_response_lower = ai_response.lower()
                if 'approve' in ai_response_lower:
                    return {
                        'decision': 'APPROVE',
                        'reason': ai_response[:200],
                        'confidence': 0.7,
                        'content_analysis': 'Text analysis only'
                    }
                elif 'reject' in ai_response_lower:
                    return {
                        'decision': 'REJECT',
                        'reason': ai_response[:200],
                        'confidence': 0.7,
                        'content_analysis': 'Text analysis only'
                    }
                    
            else:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            self.logger.error("Ollama API timeout")
        except requests.exceptions.ConnectionError:
            self.logger.error("Cannot connect to Ollama API. Is Ollama running?")
        except Exception as e:
            self.logger.error(f"Error calling Ollama: {str(e)}")
            
        return None
        
    def update_product_decision(self, product_id: int, decision: Dict[str, Any], success: bool):
        """Update product with AI decision"""
        try:
            cursor = self.db_connection.cursor()
            
            if success:
                # AI made a decision
                new_status = 1 if decision['decision'] == 'APPROVE' else 2
                query = """
                    UPDATE Product 
                    SET PStatus = ?, AIApproved = 1, AIReason = ?, 
                        AIDecisionDate = ?, RequiresManualReview = 0
                    WHERE ProductId = ?
                """
                cursor.execute(query, (
                    new_status,
                    decision['reason'][:500],  # Limit to 500 chars
                    datetime.now(),
                    product_id
                ))
                
                self.logger.info(f"Product {product_id}: AI {decision['decision']} - {decision['reason']}")
                
            else:
                # AI failed, mark for manual review
                query = """
                    UPDATE Product 
                    SET RequiresManualReview = 1, AIReason = ?
                    WHERE ProductId = ?
                """
                cursor.execute(query, (
                    "AI processing failed - requires manual review",
                    product_id
                ))
                
                self.logger.warning(f"Product {product_id}: AI failed - marked for manual review")
                
            self.db_connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error updating product {product_id}: {str(e)}")
            self.db_connection.rollback()
            
    def process_products(self):
        """Main processing function"""
        self.logger.info("Starting AI product approval process")
        
        if not self.connect_database():
            self.logger.error("Cannot proceed without database connection")
            return
            
        try:
            products = self.get_pending_products()
            
            if not products:
                self.logger.info("No pending products to process")
                return
                
            processed_count = 0
            success_count = 0
            failure_count = 0
            
            for product in products:
                try:
                    self.logger.info(f"Processing product {product['ProductId']}: {product['PName']}")
                    
                    # Create AI prompt
                    prompt = self.create_ai_prompt(product)
                    
                    # Call Ollama
                    decision = self.call_ollama(prompt)
                    
                    if decision:
                        # AI made a decision
                        self.update_product_decision(product['ProductId'], decision, True)
                        success_count += 1
                    else:
                        # AI failed
                        self.update_product_decision(product['ProductId'], {}, False)
                        failure_count += 1
                        
                    processed_count += 1
                    
                    # Small delay between requests
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error processing product {product['ProductId']}: {str(e)}")
                    self.update_product_decision(product['ProductId'], {}, False)
                    failure_count += 1
                    
            self.logger.info(f"Processing complete: {processed_count} total, {success_count} successful, {failure_count} failed")
            
        except Exception as e:
            self.logger.error(f"Error in main processing: {str(e)}")
            
        finally:
            if self.db_connection:
                self.db_connection.close()
                self.logger.info("Database connection closed")

def main():
    """Main entry point"""
    processor = AIProductApproval()
    processor.process_products()

if __name__ == "__main__":
    main() 