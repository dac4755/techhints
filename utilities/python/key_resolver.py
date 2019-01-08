#!/usr/bin/env sage

# can't remember where I got this example from but it is not my code. I
# found it while working on a ctf problem. The keys are from the ctf (pactf 2018).

import sys
from sage.all import *
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from base64 import b64decode

def product(X):
       if len(X) == 0: return 1
       while len(X) > 1:
         X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)/2)]
       return X[0]

def producttree(X):
       result = [X]
       while len(X) > 1:
         X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)/2)]
         result.append(X)
       return result

def remaindersusingproducttree(n,T):
       result = [n]
       for t in reversed(T):
         result = [result[floor(i/2)] % t[i] for i in range(len(t))]
       return result

def remainders(n,X):
       return remaindersusingproducttree(n,producttree(X))

def batchgcd_simple(X):
       R = remainders(product(X),[n^2 for n in X])
       return [gcd(r/n,n) for r,n in zip(R,X)]

def batchgcd_faster(X):
       prods = producttree(X)
       R = prods.pop()
       while prods:
         X = prods.pop()
         R = [R[floor(i/2)] % X[i]**2 for i in range(len(X))]
       return [gcd(r/n,n) for r,n in zip(R,X)]


k0 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxT9S8TtvLi24WO3H+hms\
DDssy6RGQj1V+dMNsnOIdPM52XcGC8TMLBjpSIp/yqBOo79ROUTLDTrNTFxuDr8a\
j49ZUT2RN2bACSLzVc1rNkJwkfc1Cpw3z4xNo0zNYgbsgliAOBup0ApEtfKrMDIy\
XWvQj0K6asH3lU0lxKsAHxxXWtq2Xjym+4jWMrJdoPiBeJfQGvMClFsgco31Z83i\
M7tc1yW57amoCEr7UROgH7eyAd+5gR/jPH08AJx2hd5je9LMb6cudEsqH7RFgqLt\
JkiB3oP7iat59Z1Ou11M+OH7DKW9YDXmEqGX6p05IQXVA8O7/paJgENLPOhGWfJj\
Wbi09easLJKKn1WX5xcvvyw9Gdlifx9Guur+fMheTLZFRs1wvDpJNi6qTuM+cFFx\
wZBEB+Ea2D8Lt+PUXqjEW3/OEmk/vaAtGN4Pazhb1RF1jFUd9RGapitTgiLqJTor\
39UbiHsJxRl29qHuRJ19Iovkp588QLF0/a5SHY9YTNULmFsD+qiQQvwzRGKSJ1Xw\
xRwtqxBbE9rMh8ebTBkwL+nTM4kf8zMZk/BNWmtJX6Mnh9TgPcijyfDlbGz4xOQR\
ewk07WOtzvoCeVb93Cc79g7QOMBYyOhhtV13gG+SyUfBKXe2kEmxWkLMQsKnOori\
DDab7KImDaD8t0G/VejnvdsCAwEAAQ=='

k1 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuviBSHvDUaNnOTNWvz1+\
txHyN5FlTbBXsppdBKgDc6dp5BjciOom2dDt/mNxlYzeSXtuQnFEQRolLIEdDov3\
t9IKeBIBvimIVRx7B4iDgypx92nl6d2PLht4zKnqLdH+L4cPJWQqfYUr8Zdr9zVA\
yX3HT5+QUMnyJ2mrukpGQD0c9PCGBitfESYyzpJ2UILd4aRfsB16Ql9L9aVBYdCq\
du9RTFnTRRAgYsh49CGaZLcZsWeYSvDR1GNNt0uWSNlRUibqnECuIQcrtmM3NRPn\
by2pnJ+XIbOtSAJe/nji5c+SxbBF499X5TifNCGUafIxN3EGxtqKbR7muU1mMP5v\
5Dvoc+emgByvH7SD5lwIGOvOuNFP0T5J0mH/GOnCTrfOA4sRatYoqUzUg3lGiQyl\
tHRNk1hk9SiZbsphIiyjH5jsCta8oubAcV+8umW1Gy2SqZJ1D6pQtbgrZxWQKkSl\
0LJTkR8DnKNUNxcpOhdjBuooy0LUZljGEGfj+4K2PM7Ewf+E2WEjhHFyB8KK51eC\
rBF96eB6mdJTijxf1Sjl2dPmlbYbt1KRDVREuI7BcrBY7/18GsLj8g08vwU3CoVv\
Y+lnZaH8w6oi229mqpy81m0IDE9ZTo7awoKxBqorEd8IVar9Q1QhE2P4tDY3ygAb\
m8QBOOkJgadAJGg/3CDRHEECAwEAAQ=='

k2 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArXzKqDAEBRTV1NZvfH94\
kjm43vOl7yiExaVyRaDoo3xERiTy0YDW/ciEn4XtRpEAx5Z2im1bZx+tiFuWZZdU\
QmyErBOcX665gynetCRwIFBptgfjzTF6oIAhVUx1u2JzgRzRj4occ6lA9ejiS0H3\
iqMP+lNR7dLG1KBSiLo24QnNftsYurXIftDa27+prWGN9NGxcN6WzbP67NHeNuMQ\
yk0Gm2zassdQKIQX08KdGqVDmUtz0d/QEDQqyBkcCmAkc+WWntE/VZtcKz1e64i+\
EAHabgFBw0a28tRkQLLpT1ygQ6qDXE6YtKFOnFWKxh4/nY14exMbn+CLYTv5IXms\
pksNOUXGm7kVKq8swb79zePbK9LTzhHAMisaB91n3cVmJaxhlUMDUohbkJUXTk01\
uXe5cVHhtJHYF01b7xqohQMY5iefl76Z0k+EWom0v0MYWCIs0f3S41nGRZedX8yu\
b3UxlUl8bglKeB3ONfrYaHeqlo8AlKz9SIV1sQm01JHLqMqXMhogM2JPMVdfMXQo\
G9ScJc+o0J04uACwoL3DVJR92e3mwn5APDJuwtIZcuTjJdUuAAOklISLdbHgbWNn\
cXAfLTL8Yhm90I9OUUSQatHEyS4tdkmkCewNwXx3+s46MqBHOAKzA+1qXfzWZiHd\
0TMivgdPBuvV/NcDLUQI2FMCAwEAAQ=='

k3 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAztG0Vsab/PrA9Afk3GxU\
o7W7wWrO9EbFhaB0rDTsf89CQ+FBUICwx4OR/kDIaj6BgXfyfBiJ/c3pCrq6CpE/\
/5A3lYpndKSAA1gswXXC1xnlqr8lUrLUy715hY7An6FyAGD/8cXs/q0a/j0lkpXc\
qraJq6F3jJM1hBcdKFCOn4ARmbmRaS+ASwHR/6RN99FYnLYfEvbooZr5LrfXKZpg\
Qtv0W5IEfVxlT/jdXIgNhWGLYmaRB6fux3GDkrNKNLAju93HfCornbQGOOC/d2Nu\
FE2MXpO0o4s/P57L9mZHGFzRJ4PCnSWvTcl0L+X8wMo0J+A0sZjMqNCJYkWWX5gS\
ys5CDyrrr9WsoFZsoomMI9iAl/TtXxREn8YvkvNgq8l65w0C6gYnImGUW5Jc9RFf\
gzK3Qrsl/7Qy8cjlsB8PfUdCch4KTNIrX90HtvwWkMfx2yn5KUEc3b88jazIsWI0\
/vsGDhQLafoOiZQWyGuz2Z+77SPYC2B5n7fl0qm4HTfqydS2r2UPyoyntf+xtr6o\
EA+xmlshV6yFjQEXX0lDJqhAVlhn9l2SRCOsSMPgVUKbQqvA82X4hfsqrSHRMSZk\
HsjSg0zXz2RKODnHn6j8/FXQ1A/t0+Ou1cq4gaOb/caJh6fGuCnXkOJdVcbkRSSa\
9s2Y/VvKEA1N27701XmRsMMCAwEAAQ=='

k4 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAnIOMhCaUPcsNOP0CLFnQ\
1jmQ2QDn0CxxFkiDYyj5Ar8uQhEADY/+J1GAQMWTuLebu/9sdLdjG0H2eNarJbwQ\
NdEYww9Ecy9Tas+PS5Yi0GwNs0NzBRP8FKRVloAsbuwm0oqoFbt7OTl9HNb48+Z8\
4O0RA6p9dv2G6pnbL35JgDWhwvbV8j1T/u/mSUsP5kAXGR1dHl4ftnjtK/8tqByi\
zq6JDrb+roIf9cboUJ34Ik2sysaPciO8Q7ZCGzwjrmXqabiAMtNl7kP5qgfvMYqc\
X2SXZdorWZ/51jFe2YM0z5KqwAW72A8AtDfcw+ggp/UNxD1IT/CcIMywDVcqttgH\
qfQuGlAFdPR6pbKM9E7dvZbGon5XFDUVDQ2ajJGg102FN/HF5paaJVkIEs8XpQPb\
l3++fSuBNbmMqOjZ83FeGNVZUGXgl2JCM1HIf37VKg0QtxYONlNR3uE4rBwcliug\
rWc+rY2mfHnlqL5YbSEmQUG8EZ31MsPnVW172BlRdzOGeFSm5OAG50hjqOmCokpi\
zwhx+NV7a2yBEw9wj394DhxCxb0vynRpwIoeo3xl6WbHSzUDrmF+gJBhNl8007TA\
yx2PKkuvySvFS7twuLS32TQt2jSwSJJyEEOkoGbnoK4y52tqyPDDNiOXj0UmrdZu\
fozOuZBjMJn5yVHMpQLpKscCAwEAAQ=='

k5 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArDy+96xK7NQUofnZRFVJ\
AEt9DnmPgyPxjQw2HNjktvDR3Wq/JLlCpI1CVs2xKgcji90kbcdHtT+wWTdB0ep3\
Tlq41SlQju4ma5hPGHp3FoTlc302SLbLjzgA7uHBiArd53ycRfnB0cxW/R40fs1U\
VSmBKkEMz02qeraFiAXk8Vm6GiCeMskqOcF8nkJPyi0vEi/LPoMtV4B2+tU1Jc7S\
ibn5MIUkeer3RVKQKeIfWqcgybO7+5IGWxNc9siZFc70ZyFA462wRzkJg4m1UuXM\
wSKDAxsQPQGIJJO7zXzRd2RNwxFUKzhF1MIuYNIingzl4ooS64TdVnlzQkyiHlDU\
nPvIjH4n7c4r6iKE9m0RMXCxBVUHYnPGFEQ3N46KxpRH6tkW9xzw73jmOIVa67TN\
3RGNtkMQKpuDYlQq5dUmEvTGMK4Om72NX05DcXyJr/LGGEWqcdC5hb631LHnIaAd\
XI8+YeJyNYJCZ9I6rYb4DWQMZStkG2E9W/H7k4JwdsBHxPCSaRTF9rFrM6DKP/fI\
Vecb30XPDb7tHdwMokt1rRGA9tYLZ5Pis/QC2dteLqozaaN1aPq6ugh/n4E9H9Ll\
L9sNMfDcWmopLVjXk6zp8tMNIXlC/IiQ1eqZ+L/xF1KxVwfH/gE2aHqOQJTzKy/5\
9/yB+DZ9H4WOBFZxOT1h0ycCAwEAAQ=='

k6 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvGUFUpQ8sEfwgTWkb1BT\
KzMiU3JBXqSW0AaZBlVR0HLFw9Mp1BlyaYrQGMWbUCcUd1+MejIDumi/ZDvDIYjq\
nCyVFfyQKw+VgLho/QaKg9s9tQjY4BhcYKp5niiGernn3cgn5qd1OxhJ/j25kXN8\
8D2p1HrlEzy0X3KgaBPBK4jUCA9xVWKqap+LZGsF+2QcEX0dDP64IpTJirteVhR5\
z8xzaPYWvHqsjhC4YCWU+mwbxDJXGqwY+oGgHAxjJ8aqCYAlRr2dmRX7lzd7wURJ\
FmvU3GS1XGiQg+aVV1SgXqu9m4XJPjBEgO7sGqro39pcgNYOsdAxKMCaLPfIxfys\
Uv7o9+oqyS4nuBInAAR0BxXI7Xhb/H10wE5X2FEEYSB4wLnVxwIYg5IRTZhMmskR\
TekTYNCvQYNVWew5NjTBipZgOGtboMC+AxYgDTXit7bkf2rYVPR/WmP4rpaMgJbX\
QCs+/8UYy6IETbXMn7fhVhKJ3izIVzSbgx/nwNcK3dQfP2vijzIGsxErOaLTQDAX\
XvWLkqZCi6/Q2/hgwWcMkUg86slu5KE22zxIDGJ031dL6oQTfgS38LzTBsFSLf/S\
dnvJC6kKmp8Ub39I5dw3/90q9zBuydsMMm311VqvUyFX3aSMNu1/MBFV23xUMphC\
aaqqfWUR/983KqPZ6D4f4fMCAwEAAQ=='

k7 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsqMSAjYgb+qb4mdut4sz\
61SuanAeph0cg/iWyS6svJR7hFW+bY4aUhCGRMof+z+IZH0vFKJLkIN1/IpEWrkk\
2L2vN9yLg0D20kQJhc5+MpK4xVVDLL6dhoOIcVuuaSYeFLkZ00qu7jf0z+jzSCvm\
qC+aQ+AJrcqDjcmaMIw5QyKCmo0wFlWi7MELFgNVxiAS9zI4dFeiGXCeC7sF1t+i\
+xYyKY1iN+Km0vBDQhqDg7D2OtPjYu0WbjiJG7nTAUrF8cHSkmDUWvj15ln2QHE/\
2D6CFVUj1XVDFD8kmkioj5DxVp/EdH/Q31yWBYPVgPVFojX5xeVB2Vbzm+5IA3EJ\
u80zIAsEzGd5jyO0W0+8wd8MKBBogHF/P4OmdJnHgQgDacC74UAfjj2SYirwkzU6\
6b/AD8mJ46xl05ei+UpddlhiRdVugtSf8rZ2UMLO+3YOg9X+rpHc8rxe84MsIxNP\
2msZG+OS17UhGvGT/JXRG7kgQRZPO9ZIZ93vM5YndmpSer8fnHdywfqisq2mEvT5\
NHW6s7SpaBEsQn/QxhGgICF5jBKss9fiTWDIK4qGc5dJ0oFa8EiWTsPIzH2vIddD\
93VDqkxllbO1oehbRkMPTuRn6jTMuQfx+5JeHt/upRWXuB8LWuM4MoOpYlKXg3JT\
Wr6AqiwIf/ZxnANM2hxbcRECAwEAAQ=='

k8 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAmvySm/iXzjuhPc5ylFPr\
OaI6n+eynnah4js+FP0frrMd0LOWjkmq6o/tr6Bxg09MED82JsJEowWBtKRWWgbn\
dAskNrYU5kCrV44eK+uzU2Ki7Yg/nlq/ji2o9JuV8mOb5h9B+riRIS2Y3iTJ3GFg\
CWDNA2z5Tjrh7yJ3jPbdwgMb4td0iT2cijciBCHbRSRzdPwDCj0fL1wt69xP6jOd\
fsmoNuMGy0u9PX+bhD64zd6Lvu19y2EGkLEMx94ZTJ6gG81SQOQJPCgPtlVwQ3Xj\
x8NIWiYWF3K0C67vBzmYndkwUaXjqAuLyd+LPeTWIazXm93oRn95TzJQgpko/GgA\
5i4JOumnpc3KB84wH3ACJH/fhtBnkYHTbDZgFBYMmZhNXRdR8TLHGUPkYNqXBLCt\
AJimaw4HAnl3+9YlY8OKmqnPKfNHfmzP/SEX4EbWgxsC1Tq3hCwWgHl9SIRhl3L4\
JKHLSTu6rMDVb8dgRigDx3cMxoUD8lo6WiMjl3LKdKA4g7kfAVcmvCFgU6yV86rq\
ut6IkzNbjFgY9yr8Qnxk2lRrnPmzvdB4Yxo7z4bPFDWF2SX4dSi4qW7RZCV2zOp/\
RqxqqWl/vRM6AgZLiA5LOHQwOtaHRqywAr5R96piNaXyHomFMUcVjLmqLTq/W0e3\
jDVb0YdYKkSZ3OdPECpLyWkCAwEAAQ=='

k9 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtBJ/h1aFUIrtB3NJWarO\
piWZTTlA1cOnPapmoQIO0CHX4fpjb4lHny1oglF96cNp2yVnbCheuRrV3wxXpKXf\
ZaTnYkkEVgBJ/PjwEWQqL74txOI16udDrNFa+I/Xg2zF2LBH/rEwLfljvAQeYLwt\
j6gTp0QzUSga1P9vGQ4PGMjtoQfCr5YvUDimNrXIvMFLRILkpvKVV52PsW0ZtxJ1\
yWX5ZY3uHS6CUaWctO4RTkLCpeZRVKdU4s3tPseVJv+wqTS9R5xJyGzLKU97uBNR\
yJlUn4iwogXt4Rf09Q0tMPlPZS5MppVmRBYOniCsC8Gj4ilzJD/L0tGo4hh34fGq\
QwMBkeUiJqJyiFoxzHtQx4YNrTMgJXKwX6pBmn9xGJy9MxbeLyVbr3m/vCHo7THe\
sWaOLRwJdfggSGldkBifAgJvPpID9jahVVk13100chyuwfhpYENk8p6J0gTK1JZ0\
bclgXBwU0+y7Lj42ePLRwbROygHkxmcby5RfdVSeOy9qq2RSceqB4oI0VmZjCkI+\
YhsutGvUgEBhF97TJdQhQKOqCKHJwo7klHQCALgIEr6gCA88XiidacYrFLG/Nr1A\
QDq9EZVIpRvjQ15SYb4ZMZzB/nxPZWgYjgElP1nzFOJOv/DlKdYkUI44TxRtsElj\
/bwuKRTsHy5c7mKF7S2usx0CAwEAAQ=='

k10 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAw8QzKB9j0ST8PwdLkxHq\
RgGOoj/D8eDvMm+pdAF/JseuMcQEj/sx5cJFS0r4ehnqtVOztVgDiLoWyzzaU5xd\
BOIhuu3SKQaA/nhHzNke+LsZEoQIExEqPaUReS5GQZ9g1oO/fFrX8xzU6eqcXMSZ\
nge88t/vMF7bWRFaaea+s4m958k3fgcKHI0xwk4i+ZMx4Cazn+kECnWD2OsbOjZi\
hRPV/Qxo8R0hZUUbMXemovqMVgGCzYMcXEwINA1uI1fVaguDrrbv+XXG/i7/NjDZ\
9RuTcJA8LsYvvDr6i8rGbznzJtvD9bz3yq/q6OqfYa5TfoUHOjV1qVLXZkCjubkF\
yFt2P8EZ2Q4ikzM3lQhIudINFD4P/7y/WomVFSaf1klV2SnMx151x+pYg88jSzbi\
uLj2i5R0op2vPqio8LXKFNuCb66iNZ4cN2Ltiww4dVRzGmVpJyqyVhYpmOQ5e3xm\
tqD2IfzoH+ImVf03WfZMDnBtRht9/AUW58LTfyFcs4WDQ8HfunL5RA055vLWDgKH\
olxOwWtyvB7VX4Wo1ftWULwdO/z5SHyY5mQBZ1oBbpoAchyVDTRP9oYMgSyd7EPk\
RApdioUX19nGpz/Tz+shy9q+HoEyisJHFpt4dp9+m1ZSVbFedbV5q8dZy7V7DhBs\
UDTrHAFr68zBRwxSQ9LbUF8CAwEAAQ=='

k11 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtdKuQkxe4ICHq/VgZE9j\
QXXDrT+vXUlFtmRf0cLJYg/kk7qwAgBadWBUZaQJ3VYqsijpOhevz8BQaZaCYCXc\
incujU6x5g3REjYOGZeOsFreEPVpvJC5hdlbY/YBdSQGkTMdepfUVnHkV+8zoq82\
q8ZnJwQB4hIeFMJI1D8NYAiJozJ18iXfWibgLuPLZddaaQNm2OrxsO74sw6MsKNQ\
HzdNlOX4iWL1MmJziMKOs9u4HO3AsHtnSamDMbGP1Qi9zwyl5RBAkt9UJ7njPmlO\
DhelVvKco0Ly6XfBLj+uTu74zXgBJati7KPAGL4O4N+MMGDa2WB/39b7Mad8v3Xw\
WXauQfTlcafYK/xCtSvlstTf/kmX/GTqV4nEGB+eJBadobJjy5Bo8Aa06T05K1+u\
JDSZZzzu7ezoMHSThJ3PjR7YeV3PCwF54kStTFvvNIWLWJdObKpAwM36ERvVKPrD\
Hvp3u6sl5p+3O0zj8vpKJDuWka1+FNLqk5G3XEEgmeHjdSponUt+PvxdPTa4tUCa\
BbeNcA3JjOjkFqsk4RUrkgZ39Cmab4x0Ko3nTfMtzoUP4moKUnHLpMltcJxEgepY\
r2iiurioEL1tNViXDaEszKbqfxDnbsUh1j6Tt8WKJODuJKr6YTpMdnRxp+rNb4qE\
bzF3cC3oHglux3tPvb/oSBsCAwEAAQ=='

k12 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsG19AAEB4QAaPZaTQJpv\
dFD9XByjsaxOKa/SmwezKIZapYclSZa+W3XTsbVN14eQJW9UCvB0DPqDKG16xXy2\
MGAOUIi1vlfb9hNNleV/3+/KVTL1l9ED4uhgU3cwrmHgn/ekSLmXFXHcNZyCRl7r\
FmwWw9g6KfckuaL1bN4f5AaJ7TLC6cUAUWteFOvNrNobBnu6CSw51ZSvTrv6w0EW\
/CWKusJBUXHALaWBqb4Qr+eU6PWtBF1Iii4Pn1RfICwYam1t62ujtqlB82iuxCoA\
ae/NJDJvhVBt72jhmCffmHm+KZc6QM1cR+kaf1fy67byxKj0ZD3uSKrweQhiD1Qc\
BseIPvOIU9A2EoFf8KnmykHZplfY+QbzH8qaKcnKv9PoTFElEHEzmDekwM/90/5f\
kB4oVV/j1NgtV81ZnMcToJWJUYnfpNvhdcDaVjZw5nnVC5irm3D9kZRwCFXWviZy\
RlE5eJdpV+fvDUcv8Q5/hURtFxVj/eHJGDVj/EHM582Bhf1TNLP3RrXAsTPEqT4e\
CrBOVzo07aApo5Mn+YfsaQ3JftF2KT/jy9E6lEIJd/ourHBrMe1oc2awbWHlOKuG\
EHEPNOrNuaGj3GdLpHETbXyftM/beCoTVB1XD54ui3sk5h2zs/vxJEhV6XXJx6ix\
ZW+LL56fPn9yQ/8pKhPtOqsCAwEAAQ=='

k13 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxYelodDvdxz8CmH/4bT8\
CgR254Meku7vmeKwkYJaeObPgGnLKHcUQpezhLTbkzTIja/KE5t34ty9BFDAybjL\
pKMBQ/aOVGFuRxYxlTdfAD58zcuR4iboZrq6O9R7c9S4RfaBWxefKl04V5OsRSS6\
VQIb2+eWFjx7T/hbRjUwfXzjwBU0u1fjKKF0p6W2usqF9ThroHSUlg/cToEAdX+v\
nnmtcSr2oS9V3CxAEToT/MDM1tkHqTXn1WymLTVjDRoaRhOvfejQ6AEENtw6Z3pE\
NDvI9pIAZstOrWk9tNIlVSqxYNDDgB19DYGewLa4HTh4D6i9D3X9mY6xlyz+ZrZw\
O/uyAdVQ0jZXrT3N+Gzl4KqgsAGmwG43HKzQc0KnQoESo35eHwwmjCRKfMBV8Uoi\
NlZBxLqYbGps+INTDTL/2NwN3ySEiUcP/Iqz0yfDR+ef2/k+e/j33OCaJsP7Tczs\
/AmMD9gxW8g5ZCXetY6lhyz8rjSAXbR/0lDe3GsrmgoGnewwafeAziYoq2xVybLo\
l/0nn1/m1VIaU30f93WGqNSsE8k2Acq/1SPvVEMGP6SBAVnN7u3CzJsKsSkKFFOZ\
GbwekZncLwa5tNIU2Qob9W6PV0ywDbpPS4G9UTdrRH7aABqzNJtNhUQXtKidehiO\
E8QiVFVKwZ7z3d1fmakQPRMCAwEAAQ=='

k14 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsY1qzqDWblRQQpWu0gEE\
KK1I3XeSX6DEIupHR9iLzw2eKFnyb5J3+SYGg70Y1/cWwyKyiI8RB2jhlyAabuAi\
3wUVK911pAQPRJncTFxcxiSjWwuXxkZ8JQLCiYcxTUOfIlrXXcuF78gmmrsBLAxr\
H+3I25cp26FGI8aQrWhX7fzTeN2EnN+ma1KjH86wolbszA9p94wqrgxjbs5Fpb/f\
8QGZAptx/xpmlukpPwzmQrtvS3jhoqbA9KjvK/jLmwaAAc6R5B/5pIko/cZu2Wzw\
71pwKMtnNfO1dxtEFByWjlksGw91PmFc1NenGdMZLwynjfelwVfqZ9DIaTyM7vk3\
0XiSMUqpSJhY/yTYVJ1xzjtibHTIeG2F0zut26T3AP3il5Ig+em/DlV5hWeH6pMN\
sPqW1/qmXF26YgTfeDz1N3PabC3mXk0FsDjqM1UfAW77tw9yNrkGIGV8LiRadfFB\
IrftRiYpN8Z3uBnfnxYlHncPrNz4uqI7mOFi3KN/hjp6cK9zkXZaUDYSPadAXcBt\
QcuIJB/uPpP03ZFLCH4beX3PG83sXKHJxHSQo7dOFYwYHA2E4iRcekyhS4NgtIDI\
C9wQVcdwAKIZ76xzChkVF2pB3s2LqVHXG9zALirZJUh0RJhyoJf1+NuvVqZwI9zm\
e8iaA2AbI8l1aG0I1/CwHqsCAwEAAQ=='

k15 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA4p7kfGTPpRZcwvYDgrbk\
s74dhwLXBXk/Q8NmpSyAXha5VPXavRfer7t+7EvyfS5gXC1liQGDWB0O+hdA9Qb4\
X6ymITE+M9xgnpa9igTjd8RjAdWf41JUsymH5sKmAw5ntjwn9jqz8fitt6yn2EhC\
xwqYIhWvPr1yLPYo7wYJsFDFvkVT2CqZVt9jsd0m6Xj2il2/qdRlXnXFaE5J85xh\
9zW3a0BWllgDsWrRL/WfoIJ4vD+OXvuNc04ZeA5pxkXoa+S+XtVeMxBQHpdXAcI7\
akq7Y7eq0PnETk5bhlmB5cXNu1YmH7sGo8TxFUbRbzw69W4vH/+/QTohUPwafM5m\
402+ogjCbwlsZOX8JUHqQn4NvC5KWDz7I9fzuFWfvE8ylZpQb0DIznWJczVR0WUQ\
lqJV7kKndhUesWG+qZg5Qbts9IfUmG7FjRohz3ZNMmribL5S3eCqCYW6tGkoVyjX\
Grj4KGCJxFR4s8NsLKutBxQh7htRA8snO/ulVXUdK3N7lW98+y2/AyTwp/rrFssa\
6B2vEdG8xT0ktMmiLJC+lGi7EbwvPLneQw0U6dmMw8Zyzuh6DjX+B3B0xfjTKt1S\
HSIMiq2QONhHWieTAMzLzdekm2YY4sz4HJ0h+jWKbJwf3XGc0xV3hoDJTOyC/gTq\
4g6hGJEK9UHd/oLGy3AeuacCAwEAAQ=='

k16 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsSQBzzt/EmozY5mPStn9\
ZakM9DCc7nwiSvQLk05QgoXef3xQK1oTZEzMFy1Yhs/OS9jvmoTX9ZGky4ccHdqk\
+uCqK4RVVQ62VDRKhhligocg6Ak0akgQ8Rx14/Nz9/YbQo6VJtn6CGmyhhG6YXy8\
tERTm/aOVGd1njKsarrLy2VChYISqsS7+lfWeVofl0NVUAWgblGSEEJzpNLOYnJj\
xFTYNasiwmnpAT6zyuZC07BNjuG4JW3DqtFgK8eL6wkKEmeOMVSF3nWlbBE7aBPM\
fNwwR1tvivcdfnadRDLMDCrhIoXeuh16hRl5Ps3PeFh1oA6Dp5BYGHgs3kPN334v\
nXsPfK+sFtefglrXWdWvH9bdEamupOOJ3q63oaDFfAixCdvY6pL6ztZyF2aQL4TG\
NgmKomFD9EydmV9K9MGv73xiZ22DReAAe7td8kLt4g6OHslyF7rVlxfgZqU22gOo\
5PO9Kn6B8jvz58xS4ABoBHMnzSrR2CfwYMjPZjsJ3dmg9dIaQtdH5AaH8Fx0MMl/\
WM9bmQ0In9tel/U1AU+tTLEM0n5lNa+aZfVuI+i4/N+t4szf5mk4WV2ul1o8znZ7\
NdCWhhbJ5/VSIjxU2CraApQ4JDLlZG1JiHotZ0DVrFDtenJcKdJQG/fZ7C1fOfWU\
c0FveyU0sIWBX5tYRLj7AHkCAwEAAQ=='

k17 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAuyxx2F+XvKkXAJFFj9Qz\
27FlF/gyjLEjMWAhHD4d3FRWMVvqj7dyEbwiaVYhHE4z9uEEJUxAsu2ZnLhXYvok\
3Zv9lCu9wukgijG6XVcJiVTvFwYaufbF0tM5CJr6y14y68Dy5ZELC6N2SzoSuX+T\
KmP4OBHAzZzal6b/HAXba7z1CEyKXJZcDTeJqiJTWJhCoE+WOELk3LUE5rA0VWfX\
AjK6wBPsYZ8jlXzpTlD3euAGdKOdPcTNFq6nyj994+qm6/swxqimt//te+i7TyFb\
1jn+UskJNAP6o9swUwpCDP5mbBd1ro5pgR3J+C+/lZVG6db9zD5DfoYfaPdwkxG6\
DamhKZlh5avfb4RnWRGK4aljuoxUIGQM2Zpz4QdvYN5rYO32kTd8OKZu8w8v4tdU\
rUIugDT/7CMzKSZocxuXsR+cQ8316wG/p3Hxej9UN9F1QNnpYPaGtxcCUtGslOIV\
gtRxKA1WhII5iihNHeSayTkxG4TIB30Z+RRTcbzz+MvMsg4cbwOFR+5CvtElNrW/\
PPbc59H7x0hiap15/Cj5NbfK33e0Y3cdE3FjgyKXktDGNyn1zEMZbCpT1H5aeLNi\
DLcTffY6N0vuIJbOisWjgV+rxLs+C8V6zcQfXQmMU0gimCQTwVp8OZWYNiPmupFj\
NwXqX2eaiVDELsFVKgnEVm0CAwEAAQ=='

k18 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsHws8qest63rPS6Gvs/6\
x8WD+d0i6NHwJaP1wHDmATecgg3uthTMW9NqZ13E8H9jExY6wYOXxZJi0QgtxYEg\
YdqNXxf1GVPSOuBdZBFhk6UDnRg8OB3F8enVpM1VzQ2c8h1ZyYRiaUEOGuxjVw33\
mfcx3MzOiqYkuPSwl2Gz4/SnTp554+gRjx8Ycv7qnH2Ch8XNjREBPkwegLvtREPE\
Rw9+pZhJBMbNNt7fpOTdgb4yULL+E2Zswpe7tUbmKs4UPhyd4Qt+3Xh+ntqpQwXY\
D93iueVp+mtgWMYAXOhiAxxLapDGLjuLlD3k+3W6esm/M5YW6dGEYAXBIK5Bg8Xq\
VVTE6xk4DmObl5h/Po7LQo7+SatgBYkD+kRcwrEhnLj3AMLUixqqsNIuTPnhL6qc\
oE6XBHWLXvHrZx9LoHhsv1c1amKPqvZ78nO4cnhD8m8EZuZXwhITuUqPgD7XFyVQ\
MfYbxQWn+VZrmjF8sjfXWtDMWM/8zMQN2g/GWGNcYQqWGnM0xyoPj4qb7G+Y9KYn\
/SYpjWLzJjHtKabQ/OdP9jpN5BJ7aaiUisy8peVLOORjtUbMOg4xdE+uOVnGHBWY\
3S+FvrGZj4+eH1Yfhrr6IcUY5zgb86f1EpYAvf4ARkvuW/FH5GB0H4rwumeAaKHK\
dl+DELY4jPxnRv6hlEC8BTsCAwEAAQ=='

k19 = b'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvKWuPDGGTNyQ1yIIZB9d\
6UAPfisB1qaKKrUb3P89zpRb4DCPmlm5TJV7bVDsG57VybEEA3Ng1B/aOAQvpVdt\
Bl2eRq98UHTrLDTY18W8Rq1gBS4GUYBFkA/W20uD3+nAm431X4KbFXAB4QFO0Qus\
1M64pyZqiTHFEsqUv2/lfAn53BNda0F2g7szQtvOzix1059SCQDWo/LINlVmO8xH\
0r8aOovo0qxp9+DTxeB2S5B+CvgtoFF/+ZCKdX1kJQIq7WSbvXY74T7SRqozG1J+\
AYh3dQNC2nYFK7ruJ6mJiutapqMbltbSg3FnT+TbbA6SrJ7i5RxFb7c8c6CDc7Kj\
b7mbJL5S2dSjQDuKuzBespltbmkwaGWJ6Tq2gV0fgglxAVdvplUhXMFdVCDIok9r\
MRR5WQ8KqY0c3wvXbB7504Me1Tzf9W+sfw1oUFw0a2GeRqVt80XsWU9l6jJcg/Yv\
JrbAtYI3h/UkdFueXLRhjGAxHDcdymeVU2Pbay8Pi7liP2U8tzGqP3bRLW0hrj8e\
1xxtoYUul38x9Mg+Q/vX59U3Oo3EDjUzILJlEQ4DnBRkGtaWhK6I1cPvpJKB9mjh\
tUOs+D8F8nYv2/nHngdSeL82ygxaMBvE+CrNJnE1I3HYS/7JRF0xIBLHEojF+wgP\
guHfCq0eSsidXAlZc4JB0Y8CAwEAAQ=='

k64=([k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17,k18,k19])

ktest=([RSA.importKey(b64decode(k0)).n,\
	RSA.importKey(b64decode(k1)).n,\
	RSA.importKey(b64decode(k2)).n,\
	RSA.importKey(b64decode(k3)).n,\
	RSA.importKey(b64decode(k4)).n,\
	RSA.importKey(b64decode(k5)).n,\
	RSA.importKey(b64decode(k6)).n,\
	RSA.importKey(b64decode(k7)).n,\
	RSA.importKey(b64decode(k8)).n,\
	RSA.importKey(b64decode(k9)).n,\
	RSA.importKey(b64decode(k10)).n,\
	RSA.importKey(b64decode(k11)).n,\
	RSA.importKey(b64decode(k12)).n,\
	RSA.importKey(b64decode(k13)).n,\
	RSA.importKey(b64decode(k14)).n,\
	RSA.importKey(b64decode(k15)).n,\
	RSA.importKey(b64decode(k16)).n,\
	RSA.importKey(b64decode(k17)).n,\
	RSA.importKey(b64decode(k18)).n,\
	RSA.importKey(b64decode(k19)).n])
keyse=([RSA.importKey(b64decode(k0)).e,\
        RSA.importKey(b64decode(k1)).e,\
        RSA.importKey(b64decode(k2)).e,\
        RSA.importKey(b64decode(k3)).e,\
        RSA.importKey(b64decode(k4)).e,\
        RSA.importKey(b64decode(k5)).e,\
        RSA.importKey(b64decode(k6)).e,\
        RSA.importKey(b64decode(k7)).e,\
        RSA.importKey(b64decode(k8)).e,\
        RSA.importKey(b64decode(k9)).e,\
        RSA.importKey(b64decode(k10)).e,\
        RSA.importKey(b64decode(k11)).e,\
        RSA.importKey(b64decode(k12)).e,\
        RSA.importKey(b64decode(k13)).e,\
        RSA.importKey(b64decode(k14)).e,\
        RSA.importKey(b64decode(k15)).e,\
        RSA.importKey(b64decode(k16)).e,\
        RSA.importKey(b64decode(k17)).e,\
        RSA.importKey(b64decode(k18)).e,\
        RSA.importKey(b64decode(k19)).e])

# find all the gcd's
L = batchgcd_faster(ktest)

private=([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

for i in range (0,20) :
	private[i] = ktest[i] / L[i]
	print "p["+str(i)+"]= " + str(private[i])
	print "q["+str(i)+"]= " + str(L[i])
	print "e["+str(i)+"]= " + str(keyse[i])
	


