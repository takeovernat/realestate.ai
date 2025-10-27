# Testing Guide

This guide helps you test the AI Property Matchmaker application thoroughly.

## Quick Test (2 minutes)

1. Start both servers (see QUICKSTART.md)
2. Open http://localhost:3000
3. Fill out the form:
   - Type: Single Family
   - Budget: $500,000
   - Amenities: pool, park
   - Custom: "Need home office"
4. Click "Find My Perfect Home"
5. Verify 3 results appear with match percentages

## Comprehensive Testing Scenarios

### Scenario 1: Budget Filtering
**Goal**: Verify homes above budget are excluded

**Steps**:
1. Set budget to $300,000
2. Select any type
3. Don't select amenities
4. Submit

**Expected**: Only homes ≤ $300K appear (Starter Home Plus, Urban Loft Condo, Modern Minimalist Condo)

### Scenario 2: Type Filtering
**Goal**: Verify type filtering works correctly

**Steps**:
1. Select "Condo"
2. Set budget to $1,000,000
3. Submit

**Expected**: Only condo properties appear (Urban Loft, Modern Minimalist, Luxury Penthouse)

### Scenario 3: Amenity Matching
**Goal**: Verify amenity scoring prioritizes matches

**Steps**:
1. Select "Any Type"
2. Budget: $1,000,000
3. Select: pool, gym, spa
4. Submit

**Expected**: 
- Luxury Penthouse (has all 3) should rank #1
- Sunset Retreat (has pool, spa) should rank high
- Properties with more matches rank higher

### Scenario 4: Custom Needs Text Matching
**Goal**: Verify text similarity affects ranking

**Test A - "home office"**:
1. Any type, $600,000 budget
2. Custom: "Need a home office"
3. Expected: Lakeside Villa ranks high (mentions "home office")

**Test B - "golf course"**:
1. Any type, $1,000,000 budget
2. Custom: "Love golf"
3. Expected: Golf Course Estate ranks #1

**Test C - "modern kitchen"**:
1. Any type, $500,000 budget
2. Custom: "Want modern kitchen"
3. Expected: Properties mentioning "modern kitchen" rank higher

### Scenario 5: No Matches
**Goal**: Verify error handling for no results

**Steps**:
1. Type: Single Family
2. Budget: $100,000 (unrealistically low)
3. Submit

**Expected**: Yellow warning message "No properties match your exact criteria"

### Scenario 6: Combined Scoring
**Goal**: Test multi-factor scoring

**Steps**:
1. Type: Single Family
2. Budget: $500,000
3. Amenities: pool, park, garage
4. Custom: "Need large backyard and home office"
5. Submit

**Expected**: 
- Family Haven or Lakeside Villa should rank #1
- Explanations mention matching amenities and needs
- Match percentages reflect comprehensive fit

### Scenario 7: Edge Cases

**Empty Custom Needs**:
- Leave custom needs blank
- Should still get results based on budget/amenities

**All Amenities Selected**:
- Select all 10 amenities
- Should favor properties with most amenities
- Luxury Penthouse likely ranks #1

**"Any" Type Selection**:
- Select "Any Type"
- Should return mixed property types

## API Testing

### Test Backend Directly

**Health Check**:
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy","homes_loaded":10}`

**Basic Match Request**:
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "homeType": "single-family",
    "budget": 500000,
    "amenities": ["pool"],
    "customNeeds": ""
  }'
```

**Complex Match Request**:
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "homeType": "any",
    "budget": 750000,
    "amenities": ["pool", "gym", "park"],
    "customNeeds": "Need home office and walking distance to schools"
  }'
```

**Invalid Budget**:
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "homeType": "single-family",
    "budget": -1000,
    "amenities": [],
    "customNeeds": ""
  }'
```

### Test Frontend API Route

```bash
curl -X POST http://localhost:3000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "homeType": "condo",
    "budget": 400000,
    "amenities": ["gym"],
    "customNeeds": "modern"
  }'
```

## User Experience Testing

### UI/UX Checklist

- [ ] Form inputs have clear labels
- [ ] Required fields are marked
- [ ] Budget input accepts numbers only
- [ ] Amenity chips toggle on/off visually
- [ ] Submit button shows loading state
- [ ] Results appear in clean card grid
- [ ] Match percentages display correctly
- [ ] Explanations are readable and relevant
- [ ] "Contact Agent" button is prominent
- [ ] No console errors in browser DevTools

### Responsive Design Testing

**Desktop (1920x1080)**:
- [ ] Cards display in 3-column grid
- [ ] Form has adequate spacing
- [ ] All text is readable

**Tablet (768x1024)**:
- [ ] Cards display in 2-column grid
- [ ] Form remains usable
- [ ] No horizontal scrolling

**Mobile (375x667)**:
- [ ] Cards stack in single column
- [ ] Amenity chips wrap properly
- [ ] Buttons are easily tappable
- [ ] Text remains readable

### Browser Testing

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## Performance Testing

### Load Time
- Initial page load: < 2 seconds
- Match request response: < 1 second
- No layout shifts during loading

### Network Tab Check
```
1. Open DevTools → Network
2. Submit a match request
3. Verify:
   - POST to /api/match completes
   - Response size is reasonable
   - No failed requests
```

## Error Handling Testing

### Scenario 1: Backend Offline
1. Stop the FastAPI server
2. Try submitting form
3. Expected: Error message "Unable to find matches"

### Scenario 2: Invalid Data
1. Use browser console:
```javascript
fetch('http://localhost:3000/api/match', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({invalid: 'data'})
})
```
2. Expected: 500 error handled gracefully

### Scenario 3: Network Timeout
Simulate slow network in DevTools:
1. DevTools → Network → Throttling → Slow 3G
2. Submit form
3. Verify loading state appears
4. Verify results eventually display

## Scoring Algorithm Validation

### Test Score Calculation

**Budget Score Validation**:
- Property at 80% of budget should score ~1.0
- Property at 50% of budget should score ~0.85
- Property at 95% of budget should score ~0.85

**Amenity Score Validation**:
- 3/3 amenities matched = ~1.0 amenity score
- 2/3 amenities matched = ~0.67 amenity score
- 0/3 amenities matched = 0.0 amenity score

**Custom Needs Validation**:
- Text containing exact keywords should score higher
- Semantic similarity should be captured
- Empty custom needs should give neutral score

## Regression Testing Checklist

After any code changes, verify:

- [ ] All 10 homes load correctly
- [ ] Form validation works
- [ ] Type filtering works
- [ ] Budget filtering works
- [ ] Amenity scoring works
- [ ] Custom needs matching works
- [ ] Top 3 results returned
- [ ] Explanations generate correctly
- [ ] UI remains responsive
- [ ] No console errors
- [ ] CORS still configured
- [ ] API endpoints respond

## Automated Testing (Future)

### Frontend Tests (Jest + React Testing Library)
```typescript
// Example test structure
describe('PreferenceForm', () => {
  it('validates required fields', () => {});
  it('submits form data correctly', () => {});
});

describe('HomeCard', () => {
  it('displays property information', () => {});
  it('formats price correctly', () => {});
});
```

### Backend Tests (pytest)
```python
# Example test structure
def test_health_endpoint():
    """Test /health returns 200"""
    pass

def test_match_endpoint():
    """Test /match with valid data"""
    pass

def test_score_calculation():
    """Test scoring algorithm"""
    pass
```

## Common Issues & Solutions

### Issue: No results returned
**Check**:
1. Is budget too low?
2. Is type filter too restrictive?
3. Are backend and frontend running?

### Issue: CORS errors
**Solution**: 
- Verify backend CORS settings include http://localhost:3000
- Check both servers are on correct ports

### Issue: Scores seem wrong
**Debug**:
1. Check console for matcher.py logs
2. Verify amenity matching logic
3. Test with simpler inputs

### Issue: Slow responses
**Check**:
- Backend processing time
- Network latency
- Consider adding caching

## Documentation Testing

Verify all documentation is accurate:
- [ ] README installation steps work
- [ ] QUICKSTART commands work
- [ ] API examples in docs return correct responses
- [ ] Deployment guide references are current

---

## Test Coverage Summary

| Component | Test Coverage |
|-----------|---------------|
| Frontend Form | Manual ✓ |
| Backend API | Manual ✓ |
| Scoring Algorithm | Manual ✓ |
| UI/UX | Manual ✓ |
| Error Handling | Manual ✓ |
| Responsive Design | Manual ✓ |

**Recommendation**: Add automated tests before production deployment.
