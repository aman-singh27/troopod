## AdaptLP API Tests

### Test Case 1 — Happy Path (Image Upload)
```
Input:
  ad_image: a product ad image (any brand — shoes, skincare, electronics)
  lp_url: https://troopod.io

Expected:
  - Response status 200
  - modifications array has 3-8 items
  - modified_html contains <base href="https://troopod.io">
  - At least one modification has element_type = "h1"
  - personalization banner present in modified_html
  - Preview iframe renders the Troopod page with modified headlines
```

### Test Case 2 — Happy Path (Ad URL)
```
Input:
  ad_url: any live product page URL (used as ad creative)
  lp_url: https://troopod.io

Expected:
  - Backend successfully screenshots the ad_url
  - Same result structure as Test Case 1
  - No error about screenshot failure
```

### Test Case 3 — Invalid LP URL
```
Input:
  ad_image: [valid image]
  lp_url: https://this-website-does-not-exist-xyz123.com

Expected:
  - 422 response
  - Error message: "Could not fetch the landing page. Check the URL."
  - Frontend shows error state, not crash
```

### Test Case 4 — Large Image Upload
```
Input:
  ad_image: image > 5MB
  lp_url: any valid URL

Expected:
  - Frontend rejects before upload with message "Image must be under 5MB"
  - No API call made
```

### Test Case 5 — Neither Ad Input Provided
```
Input:
  lp_url: https://troopod.io
  (no ad_image, no ad_url)

Expected:
  - Frontend form validation prevents submission
  - Error: "Please provide an ad image or URL"
```

### Test Case 6 — X-Frame-Options Block
```
Input:
  ad_image: [valid image]
  lp_url: https://google.com  (blocks iframes)

Expected:
  - API returns modified HTML successfully  
  - Frontend iframe shows blank/blocked
  - Fallback message shown: "This page blocks preview. Download the HTML to view locally."
  - Download button still works
```

### Test Case 7 — Gemini Rate Limit (Free Tier)
```
Simulate by sending 16+ requests within 1 minute.

Expected:
  - Backend catches 429 from Gemini
  - User sees: "AI service is busy. Please wait 30 seconds and try again."
  - No crash, no 500 with stack trace
```

### Test Case 8 — Mobile Responsive
```
Resize browser to 375px width (iPhone SE)

Expected:
  - Input form stacks vertically
  - Ad input + LP input in single column
  - Buttons full width
  - Result page: modifications panel + iframe scrollable
  - No horizontal overflow
```
