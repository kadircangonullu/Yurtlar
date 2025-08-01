using System;

namespace Yurtlar
{
    /// <summary>
    /// Partial class extension for Product to add AI approval system properties
    /// This file is separate from the auto-generated Product.cs to avoid conflicts
    /// </summary>
    public partial class Product
    {
        // AI Approval System Properties
        public bool? AIApproved { get; set; }
        public string AIReason { get; set; }
        public DateTime? AIDecisionDate { get; set; }
        public bool RequiresManualReview { get; set; } = false;
        
        // Helper properties for UI
        public string AIStatusText
        {
            get
            {
                if (RequiresManualReview)
                    return "Manual Review Required";
                if (AIApproved.HasValue)
                    return AIApproved.Value ? "AI Approved" : "AI Rejected";
                return "Pending AI Review";
            }
        }
        
        public string AIStatusClass
        {
            get
            {
                if (RequiresManualReview)
                    return "text-warning";
                if (AIApproved.HasValue)
                    return AIApproved.Value ? "text-success" : "text-danger";
                return "text-muted";
            }
        }
        
        public string AIDecisionIcon
        {
            get
            {
                if (RequiresManualReview)
                    return "fas fa-exclamation-triangle";
                if (AIApproved.HasValue)
                    return AIApproved.Value ? "fas fa-robot text-success" : "fas fa-robot text-danger";
                return "fas fa-clock";
            }
        }
    }
} 