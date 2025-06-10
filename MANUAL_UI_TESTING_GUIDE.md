# Manual UI End-to-End Testing Guide
**Date:** June 9, 2025  
**Purpose:** Complete UI-driven workflow testing with live data verification

## 🎯 Overview

This guide walks you through manually testing the complete end-to-end workflow:
1. **Frontend UI** → Create experiment via React interface
2. **Analysis Execution** → Run text analysis through the UI
3. **Results Display** → View results in Analysis Results tab
4. **Database Verification** → Confirm data persistence in PostgreSQL

## 🚀 Prerequisites

**Services Running:**
- Frontend: http://localhost:3000 (React dev server)
- API: http://localhost:8000 (FastAPI server)
- Database: PostgreSQL running on localhost:5432

**Start Services:**
```bash
# Terminal 1: API Server
python launch.py --api-only

# Terminal 2: Frontend
cd frontend && npm run dev
```

## 📝 Manual Testing Steps

### Step 1: Access the Frontend
1. Open browser to http://localhost:3000
2. Verify page loads with "Narrative Gravity Wells - Research Workbench" title
3. Should see the experiment designer interface

### Step 2: Configure Experiment
1. **Prompt Template:** Select "Civic Virtue Analysis v2.1"
2. **Framework Configuration:** Select "Civic Virtue Framework" 
3. **Scoring Algorithm:** Select "Hierarchical Scoring v2.1"
4. **Analysis Mode:** Leave as "Single Model" or choose "Multi-Model"
5. **Model Selection:** Ensure "gpt-4" is selected

✅ **Expected:** All dropdowns should populate with real data from the API

### Step 3: Input Text for Analysis
1. In the text area, paste this test text:
```
In these challenging times, we must choose between hope and despair, between unity and division. 
Our democracy depends on the active participation of all citizens. We have the power to build 
a more just and equitable society for everyone. The path forward requires courage, truth, and 
a commitment to justice. We cannot allow fear and manipulation to divide us. Instead, we must 
embrace our shared dignity and work together toward a better future for all.
```

### Step 4: Execute Analysis
1. Click "Run Analysis" button
2. Should see analysis progress indicator
3. Wait for completion message: "Analysis complete! Check the Analysis Results tab."

✅ **Expected:** Analysis completes successfully within 30 seconds

### Step 5: View Results in UI
1. Click on "Analysis Results" tab
2. Should see "Analysis Result #1" card displayed
3. Verify the following elements are visible:
   - **Model used:** gpt-4
   - **Execution time:** Recent timestamp
   - **Well scores:** Bar chart or numerical display
   - **Calculated metrics:** Elevation, Polarity, Coherence, Directional Purity
   - **Top scoring wells:** Should show 3 highest wells

✅ **Expected:** Complete results visualization with all metrics

### Step 6: Verify Database Data
1. Open new terminal and run:
```bash
# Check experiments
curl -s http://localhost:8000/api/experiments | python -m json.tool

# Get the experiment ID from output, then check runs
curl -s http://localhost:8000/api/experiments/[ID]/runs | python -m json.tool

# Verify run details
curl -s http://localhost:8000/api/runs/[RUN_ID] | python -m json.tool
```

✅ **Expected Database Data:**
- **Experiment:** Properly configured with template/framework/algorithm IDs
- **Run:** Complete with text content, scores, status="completed", success=true
- **Raw Scores:** 10 wells with values between 0.0-1.0
- **Hierarchical Ranking:** Primary wells with relative weights
- **Calculated Metrics:** All four metrics present with valid values

## 🔬 Advanced Testing

### Multi-Model Analysis
1. Configure experiment as above
2. Toggle "Multi-Model Mode" if available
3. Select multiple models (e.g., gpt-4, claude-3-sonnet)
4. Run analysis
5. Verify multiple result cards appear (one per model)

### Result Interaction Testing
1. After analysis, try pinning/unpinning results
2. Expand/collapse detailed sections
3. Test filtering if available
4. Verify data persists across tab switches

### Error Handling Testing
1. Try running analysis without configuring experiment
2. Try with empty text input
3. Verify appropriate error messages appear

## 🎯 Success Criteria

**✅ Complete Success When:**
1. **UI Configuration:** All dropdowns load real data
2. **Analysis Execution:** Completes without errors
3. **Results Display:** Shows complete analysis with visualizations
4. **Database Persistence:** All data correctly stored
5. **Data Quality:** 
   - Raw scores for all expected wells (Dignity, Truth, Justice, Hope, Pragmatism, etc.)
   - Hierarchical ranking with primary wells
   - Calculated metrics within expected ranges
   - Complete provenance and metadata

## 🐛 Troubleshooting

### Common Issues:
1. **Empty dropdowns:** API server not running or CORS issues
2. **Analysis fails:** Check browser console for errors
3. **No results display:** State management issues
4. **Database empty:** API integration problems

### Debug Commands:
```bash
# Check API health
curl http://localhost:8000/api/health

# Check configuration endpoints
curl http://localhost:8000/api/framework-configs
curl http://localhost:8000/api/prompt-templates
curl http://localhost:8000/api/scoring-algorithms

# Check browser console for errors
# Open browser Dev Tools → Console tab
```

## 📊 Expected Well Scores

For the test text provided, you should see scores similar to:
- **High scores (0.6-0.8):** Hope, Truth, Dignity, Justice
- **Medium scores (0.3-0.6):** Pragmatism
- **Low scores (0.1-0.4):** Fear, Manipulation, Tribalism, Resentment

## 🎉 Completion

When all steps pass successfully, you have verified:
✅ **Complete UI-to-Database Workflow**  
✅ **Live Data Integration**  
✅ **Analysis Quality**  
✅ **Results Visualization**  
✅ **Data Persistence**

**Your frontend is fully functional with live data!** 🎊 