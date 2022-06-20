# Blue button information

## Auth2.0

1. Client ID: OGfThHF00Xa1j9P1WxAMlPGS2PP4GNSv89tdv3fd
2. Client Secret: u8G915ychSq8Go8FuVE8B8T56arSdbNk7Kj3fobNXt9BEv75SLXjdncCOfddAzijTiIiCEAOwN9f5RjNDg0gUX3viG2S3FC09txeDhcAQxfvBxMSf3PaaOofF73zl0jl

## Client Test

Tutorial link:

```
https://bluebutton.cms.gov/developers/
```

Authorization Link:

```
https://sandbox.bluebutton.cms.gov/v2/o/authorize/?response_type=code&client_id=9FTkjlaFygjcy4KAqxRZoDHUCK4MHCptUSOIoZUa&redirect_uri=https%3A%2F%2Fsandbox.bluebutton.cms.gov%2Ftestclient%2Fcallback&state=JGlpA2khtILA0ARFD4IaFEvhvs1scz
```

Sample user access:

```
You'll need sample beneficiary credentials to log in

The first user is BBUser00000 with password PW00000! and these sample users continue all the way to BBUser29999 with password  PW29999!
Note: the ! at the end of the password is required
```

User sample:

```
User: BBUser00000
Pass: PW00000!

...

User: BBUser29999
Pass: PW29999!
```

Patient:

```
{'access_token': 'eipGr4VuRi54Pw6Rlej7eL3qwPfnUC', 'expires_in': 36000, 'token_type': 'Bearer', 'scope': ['introspection', 'patient/Coverage.read', 'patient/ExplanationOfBenefit.read'], 'refresh_token': '9GxD75y2o4tgbdYePXc2P0fIw9ZOPk', 'patient': '-19990000000001', 'expires_at': 1655745962.111472}
```

OAuth2 authorization:

```bash
curl https://sandbox.bluebutton.cms.gov/v2/o/authorize/?response_type=code&client_id=OGfThHF00Xa1j9P1WxAMlPGS2PP4GNSv89tdv3fd&scope=patient%2FCoverage.read%20patient%2FExplanationOfBenefit.read&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback
```
