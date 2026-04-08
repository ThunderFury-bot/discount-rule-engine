# 🚀 EXECUTION GUIDE — Browser & Terminal

## PART 1: START THE FLASK SERVER

### Terminal (Windows PowerShell)
```powershell
# Navigate to project directory
cd c:\Users\Admin\Desktop\discount_assignment

# Activate virtual environment
.venv\Scripts\activate

# Start Flask server
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## PART 2: TEST IN BROWSER

### Try These URLs (after Flask is running):

#### 1️⃣ Health Check
```
http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Discount Rule Engine API is running"
}
```

---

#### 2️⃣ Get All Rules
```
http://localhost:5000/rules
```

**Expected Response:**
```json
{
  "rules": [
    {
      "name": "Rule 1: New customer — 10% discount",
      "priority": 1
    },
    {
      "name": "Rule 2: Large order (>₹10,000) — flat ₹500 discount",
      "priority": 2
    },
    {
      "name": "Rule 3: Wednesday special — 5% discount",
      "priority": 3
    }
  ]
}
```

---

#### 3️⃣ Apply Discount (POST Request)
Cannot be tested directly in browser address bar, use cURL in terminal instead (see below).

---

## PART 3: TEST IN TERMINAL (cURL Commands)

**Keep Flask server running in one terminal, use another terminal for cURL commands:**

### Terminal Tab 2 (For Testing)
```powershell
# Navigate to project directory
cd c:\Users\Admin\Desktop\discount_assignment
```

---

### Test Case 1: NEW Customer (Rule 1 - 10% Discount)
```powershell
Test Case 1 — NEW Customer
$body = @{
    customerType = "NEW"
    dayOfWeek = "MONDAY"
    items = @(
        @{
            productId = "P001"
            category = "Electronics"
            price = 1000
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://127.0.0.1:5000/apply-discount" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

**Expected Output:**
```json
{
  "applied_rule": "Rule 1: New customer — 10% discount",
  "discount_amount": 100.0,
  "final_amount": 900.0,
  "order_total": 1000.0,
  "original_total": 1000.0,
  "rule_priority": 1,
  "success": true
}
```

---

### Test Case 2: REGULAR Customer - Large Order (Rule 2 - ₹500 Discount)
```powershell
Test Case 2 — REGULAR Customer (Large Order)
$body = @{
    customerType = "REGULAR"
    dayOfWeek = "WEDNESDAY"
    items = @(
        @{
            productId = "P001"
            category = "Electronics"
            price = 8000
        },
        @{
            productId = "P002"
            category = "Clothing"
            price = 7000
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://127.0.0.1:5000/apply-discount" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

**Expected Output:**
```json
{
  "applied_rule": "Rule 2: Large order (>₹10,000) — flat ₹500 discount",
  "discount_amount": 500.0,
  "final_amount": 14500.0,
  "order_total": 15000.0,
  "original_total": 15000.0,
  "rule_priority": 2,
  "success": true
}
```

---

### Test Case 3: PREMIUM Customer - Wednesday (Rule 3 - 5% Discount)
```powershell
Test Case 3 — PREMIUM Customer (Wednesday)
$body = @{
    customerType = "PREMIUM"
    dayOfWeek = "WEDNESDAY"
    items = @(
        @{
            productId = "P001"
            category = "Furniture"
            price = 8000
        }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://127.0.0.1:5000/apply-discount" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

**Expected Output:**
```json
{
  "applied_rule": "Rule 3: Wednesday special — 5% discount",
  "discount_amount": 400.0,
  "final_amount": 7600.0,
  "order_total": 8000.0,
  "original_total": 8000.0,
  "rule_priority": 3,
  "success": true
}
```

---

## PART 4: RUN AUTOMATED TESTS

### 4A. Unit Tests (Terminal)
```powershell
cd c:\Users\Admin\Desktop\discount_assignment
.venv\Scripts\activate
python test_engine.py
```

**Expected Output:**
```
=======================================================
   RUNNING DISCOUNT ENGINE TEST SUITE
=======================================================

[PASS] Test 1 PASSED — Rule 1 applied
[PASS] Test 2 PASSED — Rule 2 applied
[PASS] Test 3 PASSED — Rule 3 applied
[PASS] Test 4 PASSED — Boundary test

Ran 4 tests in 0.002s

[SUCCESS] ALL 4 TESTS PASSED
```

---

### 4B. API Integration Tests (Terminal - with Flask Running)
```powershell
# In a separate terminal:
cd c:\Users\Admin\Desktop\discount_assignment
.venv\Scripts\activate

# Make sure Flask is running in another terminal first!
python test_api.py
```

**Expected Output:**
```
============================================================
TEST 1: NEW Customer (should apply Rule 1 - 10% discount)
============================================================
{
  "applied_rule": "Rule 1: New customer — 10% discount",
  "discount_amount": 100.0,
  "final_amount": 900.0,
  ...
}

============================================================
TEST 2: Large Order ₹15,000 on WEDNESDAY
============================================================
{
  "applied_rule": "Rule 2: Large order (>₹10,000) — flat ₹500 discount",
  "discount_amount": 500.0,
  "final_amount": 14500.0,
  ...
}

============================================================
TEST 3: PREMIUM Customer - Wednesday - Rule 3 (5% discount)
============================================================
{
  "applied_rule": "Rule 3: Wednesday special — 5% discount",
  "discount_amount": 400.0,
  "final_amount": 7600.0,
  ...
}

============================================================
All API tests completed successfully!
============================================================
```

---

## QUICK REFERENCE

### 🌐 BROWSER URLs (with Flask running)
| Endpoint | URL | Method |
|----------|-----|--------|
| Health Check | `http://localhost:5000/health` | GET |
| List Rules | `http://localhost:5000/rules` | GET |
| Apply Discount | `http://localhost:5000/apply-discount` | POST |

### 💻 TERMINAL COMMANDS
| Task | Command |
|------|---------|
| Start Flask | `python app.py` |
| Run Unit Tests | `python test_engine.py` |
| Run API Tests | `python test_api.py` (needs Flask running) |
| Stop Flask | `CTRL+C` |

---

## COMPLETE WORKFLOW (Step-by-Step)

### Step 1: Open Terminal 1
```powershell
cd c:\Users\Admin\Desktop\discount_assignment
.venv\Scripts\activate
python app.py
```
✅ Flask now running on `http://localhost:5000`

### Step 2: Test in Browser
1. Visit: `http://localhost:5000/health` 
2. Visit: `http://localhost:5000/rules`

### Step 3: Open Terminal 2 (Keep Flask running in Terminal 1)
```powershell
cd c:\Users\Admin\Desktop\discount_assignment
.venv\Scripts\activate
python test_api.py
```

### Step 4: Run Unit Tests (Terminal 2)
```powershell
python test_engine.py
```

### Step 5: Test with cURL (Terminal 2)
```powershell
curl -X POST http://localhost:5000/apply-discount `
  -H "Content-Type: application/json" `
  -d '{"customerType":"NEW","dayOfWeek":"MONDAY","items":[{"productId":"P001","category":"Electronics","price":1000}]}'
```

---

## TROUBLESHOOTING

**Issue:** "Python not found"
```powershell
# Use full path to Python
.venv\Scripts\python app.py
```

**Issue:** "Port 5000 already in use"
```powershell
# Kill the process using port 5000
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process
```

**Issue:** "Module not found"
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

---

## TESTING CHECKLIST

- [ ] Flask server starts successfully
- [ ] Health endpoint returns `healthy` status
- [ ] Rules endpoint lists 3 rules
- [ ] Test Case 1: NEW customer gets 10% discount
- [ ] Test Case 2: REGULAR customer gets ₹500 flat
- [ ] Test Case 3: PREMIUM customer gets 5% on Wednesday
- [ ] Unit tests: 4/4 pass
- [ ] API tests: 3/3 pass
- [ ] All cURL requests return success

---

**Ready to execute? Start with Part 1 above! ✅**
