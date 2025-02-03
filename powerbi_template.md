## Power BI Report Requirements Template

**1. Report Overview**  
- **Business Objective**: [Brief description of the core problem/decision the report addresses]  
- **Primary Audience**: [Executive/Managerial/Operational roles]  
- **Frequency**: [Real-time/Daily/Weekly/Monthly]  
- **Security Requirements**: [Row-level security, data sensitivity, access restrictions]  

---

**2. Data Source Specifications**  
*Table 1: Data Source Details*

| Server Name | Database | Table/View | Key Columns Needed | Refresh Frequency | Owner Contact |
|-------------|----------|------------|---------------------|-------------------|--------------|
|             |          |            |                     |                   |              |

*Requirements*:  
- SQL queries : [If have any]
- Historical data needed: [Time range]  
- Existing queries to reuse: [Attach examples]  

---

**3. Dashboard Structure**  
*Table 2: Tab/Dashboard Layout*

| Tab Name | Purpose | Key Metrics | Target Audience | Priority (High/Med/Low) |
|----------|---------|-------------|-----------------|--------------------------|
|          |         |             |                 |                          |

---

**4. Visual Specifications**  
*Table 3: Visual Requirements*

| Visual Type | Purpose | Logic/Calculation | Source Columns | Filters Needed | Complexity (1-5) | Business Impact (High/Med/Low) |
|-------------|---------|--------------------|----------------|----------------|-------------------|--------------------------------|
|             |         |                    |                |                |                   |                                |

*Example*:  
- **Visual Type**: Sales Trend Map  
- **Logic**: "Sales Amt = SUM(Sales[Amount]) filtered by selected region"  
- **Complexity**: 4 (Requires custom DAX for dynamic region grouping)  
- **Impact**: High (Used for territory expansion decisions)  

---

**5. Complexity & Business Impact Assessment**  
- **Technical Complexity Drivers**:  
  - Custom DAX formulas required  
  - Data blending from >3 sources  
  - Real-time data processing  
- **High-Impact Visuals**:  
  - Those used in executive presentations  
  - Visuals triggering immediate actions (e.g., inventory alerts)  

---

**6. Additional Requirements**  
- **Export/Print Requirements**: [PDF/Excel formats, specific layouts]  
- **Integration Requirements**: [Power Apps embedding, Teams integration]  

---

**Approval & Sign-off**  
| Role          | Name | Approval Date | Notes |
|---------------|------|---------------|-------|
| Business Owner|      |               |       |
| Technical Lead|      |               |       |

---
