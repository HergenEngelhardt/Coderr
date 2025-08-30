# Token Authentication Troubleshooting Guide

## Problem: Auth Token wird nicht korrekt übergeben

### 1. CORS Headers fehlen möglicherweise
Das könnte in Frontend-Anwendungen ein Problem sein.

### 2. Korrekte Header-Formatierung
- ✅ Korrekt: `Authorization: Bearer <token>`
- ❌ Falsch: `Authorization: Token <token>`
- ❌ Falsch: `Authorization: <token>`
- ❌ Falsch: `Token: <token>`

### 3. Token Storage Issues
- Token muss nach Registration/Login gespeichert werden
- Token muss bei jedem API-Call mitgesendet werden
- Token darf nicht verändert werden (kein Trim, etc.)

### 4. Common JavaScript/Frontend Issues:

```javascript
// ✅ Korrekt:
const token = localStorage.getItem('token');
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

// ❌ Häufige Fehler:
const headers = {
    'Authorization': token,  // Missing "Bearer "
    'Token': token,          // Wrong header name
    'auth': token           // Wrong header name
};
```

### 5. Python/Requests Issues:

```python
# ✅ Korrekt:
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
response = requests.get(url, headers=headers)

# ❌ Häufige Fehler:
headers = {
    'Authorization': token,  # Missing "Bearer "
    'auth': token           # Wrong header name
}
```

### 6. cURL Examples:

```bash
# ✅ Korrekt:
curl -H "Authorization: Bearer <your-token>" http://127.0.0.1:8000/api/offers/

# ❌ Falsch:
curl -H "Token: <your-token>" http://127.0.0.1:8000/api/offers/
```

### 7. Debugging Steps:

1. **Verify token is received after login/registration**
   - Check if token field exists in response
   - Verify token is not empty or null

2. **Verify token is stored correctly**
   - Check localStorage/sessionStorage in browser
   - Check variables in your code

3. **Verify token is sent correctly**
   - Check Network tab in browser dev tools
   - Look for Authorization header in outgoing requests

4. **Verify token format**
   - Must start with "Bearer "
   - Token should be a long string (JWT format)

### 8. Django Settings Check

Make sure these settings are correct in settings.py:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}
```

### 9. Test with working example:

Use the test scripts in this repository:
- `test_token_issue.py` - Basic token test
- `detailed_token_test.py` - Detailed analysis  
- `token_expiration_test.py` - Token validity test

All of these scripts work correctly, so compare your implementation with them.
