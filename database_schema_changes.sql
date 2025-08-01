-- AI Approval System Database Schema Changes
-- Run this script on your Azure SQL Database

-- Add new columns for AI tracking
ALTER TABLE Product ADD AIApproved bit NULL;
ALTER TABLE Product ADD AIReason nvarchar(500) NULL;
ALTER TABLE Product ADD AIDecisionDate datetime NULL;
ALTER TABLE Product ADD RequiresManualReview bit DEFAULT 0;

-- Add indexes for better performance
CREATE INDEX IX_Product_PStatus_RequiresManualReview ON Product(PStatus, RequiresManualReview);
CREATE INDEX IX_Product_AIDecisionDate ON Product(AIDecisionDate);

-- Update existing products to have default values
UPDATE Product SET 
    AIApproved = NULL,
    AIReason = NULL,
    AIDecisionDate = NULL,
    RequiresManualReview = 0
WHERE AIApproved IS NULL;

-- Verify the changes
SELECT 
    COUNT(*) as TotalProducts,
    SUM(CASE WHEN PStatus = 0 THEN 1 ELSE 0 END) as PendingProducts,
    SUM(CASE WHEN RequiresManualReview = 1 THEN 1 ELSE 0 END) as ManualReviewNeeded,
    SUM(CASE WHEN AIApproved = 1 THEN 1 ELSE 0 END) as AIApprovedProducts
FROM Product; 