import os
import requests
import pandas as pd

# ==============================
# API SETTINGS
# ==============================
url = "https://api.apiit.edu.my/staff/listing"

headers = {
    "Authorization": "Bearer H4sIAKFV2GoC/+16XXOjypLtL5oJCoTn6NFYFAiLwhT1AfUyAZTaCAoJW9hC/PpJJHdP947dZ2afO3Nj7seDw4EKFZWZKzPXSrS/Rk0V1IfkEG35vEXksD1vj9Stn7YP227IxVO0/uf9NbIqezSVWbeFJCeVweJxrKvD4+v2yau3HW4LW8w1op+lLT7y5cvh9/X7X/4UHchcXMlmuyKZ5RQ2X+0YPZAgHpMNbZMn6xIHqaU23oH08UwC/hEHyqjN41yweCSbx6t6sizSxvNO+qvCTsck2M7x5nUVt9srYcTs5PSpbPOx69FQONFnba97Haw/qsB8qMxtK9sa4fytyskMn78ruRoV6+yiTacEzhHbhUuullW0Xr+T2ylu0zGW5BDb25lsdBNvlNkxr1cyvcS2P+8Y/O9TOFsxx1fUJAHpdqw5xPPjKtlsr3HLZ5WhY92vUf3kXpXE3a7H5+rJu38WIFPJyNSHX9Y+60B8lDJ9rcPoU/XmrDIP1ba47o6RKeBzJVFTyqnetqfXPZo+vvv4J1+3dS86JV2rlPicOxDQQNzuhzWvsImpHcLvMb0cdvhP95iVJFeV0+/fM3t+uijReCVfD1k3yljggfnkWUvwvxxKbnV2JqdzZqGtChsifIVEJzLdR2Plr7no+LUQTRYLIoUZRMyjTAr9XAa4KIP1S4YHR2y8di+KKeuQpA657V8GUVjY5qXkAxP5EMXcHbKcRFVfT8onEenMR9YKWvXaYv0ga0HHhFFGcRQKIU6qcz/qoGnLWUxScFRxd3P7fk4vsvsHv992Hyo3cDaac7mczTiMU09byE9zTfbM+7qe+HJNfWzJfFjWN3F4u/7lfri+2VoH8cxu+w2fym8ybZOHylFxbK0uhdOh2MY5kSNgkj6wwEJVQDdJqMtKqHfYLyl95MYbD/Yb3hmmNO7QA8upEkHzJrv4QrB5Y7l+oYF2mVx8aV1FrqIy10MhdBD75q1ymmTfjy4zVO05eiudIU6tAUmJFMT+jTLyIvxuAl9Fe77mbPGlKKzCWnyJeDELUhp+hXWy79xB20YJy327xwptvq7dTA6fJUfsFguu3grbJbD/ubZNS9HwDjF/Vv60yfqmEXMzMLhOjZK0izo+v1rSiCA1WFCjy30XPRcz+A+TMclpu+8Gi8kxyBDBrCO7eIO3TOhEc/S+D0ZRouGqeI0qHI3CNG3VbW0ph26PdSC6dRMfveeC4Qvx10L7k5LBxZb9eWJIhTSPGu7QkrfRJesuk3JUSfuGFYxIKvGoZ8yEBbkSni4JN3f7Z7zYeykAa2lLSvBnd8c22aY9fN+eHgpLr8pAQHybg0DiZm+FDYvhXNQeLSmap31PQtpDrs34oZi3K+0v+Glu8VvWNeDjjsfhzBAtS+76gGQFeHyQ/fAeAx55bwhFxgJ78R6wHIeNijvzANck9ldXmuukEmL4cb6jV1JriY9ZcuWNSrPg4QNyuayC6JzkYrHvfIunULj0B1kF0xO3yFMK/kmlFnEw5VyIVWbou/Ijzi0zZxKdS5tuq1BHZb8eFG6SKiD33JaTA7UhK224ZoDPTqyYiK0FjzQXCeAXMQF2dTf/HgA/gIdbLp95ZxjUlxKed1QIs0TgiHbus+jHgAkiCG+oYN69dvU//DWw4wB4d/2M0YTPj7NkkSD+zV8JtZDFLJqV3fqev8iH2kGfwL8jy4eEIvG1X/SRHk0J/uiLOTqXFuSTbQT4fwX5CFhazk+JwGbFOnok3IV8wUk6w7qgZKkHgGNYxxZct9pa+1DzIB/jK7Piy953Ie4RmGTuz7OjkLYexHmpvQPkD+TLUXfCnt6/8utWf8BPS71JIF+4gPiWHYLnk6i2oPb165v/wb8oNRpXfrTUF6p8kRGOBPiOQPxtBbV936fXChAlnIbK9nG65V8XUcHVE/g7iNGv16nxLxBvWTqPCK6xvudDG3euc8fLds6OqpM+RkIiWeJhQ3h0oI4+8nbxJy3Szl38OUjTRFqIUfRNmc7iqei0o6A3p/10ALy8ZxzyA3qRPHoHiMcR8vqGJ4h4KSwF61pqbPIqJPd69+/xgXrpL/WN7oUZl/iU/TQu9RLqVygYjRfLWI+W+OWcwXpnXVgbQbzWPGX0az8ioQ8s+8kS+ZNs/dVe0o/SaYzggyy6eFLm9cKXGAjoB1BfSqQ5O4qGcvUgWuLFiGyzbk1jw2fZT50OoG4s+WCic9GjQEsaJDngy6aXot0iteDiqFr6VS9SI77f/723vaU9KgWCfsMivO8Az4CHCp4P+IP8gX4hmxdquUu/OAFeHsCeF+qbpT+IPcDsvp9CkO9BLAb5h3wP0qWf+NYV8FWmMsop+B/icyqsRmgx5LzFccV8lEnjlBLieRQ3vAFD8RZ8w7kIxYNXGB3UQbSB+tdmWCBpdBbzaYyZuPkX6kNW+/d4ldCrhRVPdU8KakQG9ZCwTjxXNv0QLe3EbAB/d3yDH9uv/AD8oXvv75fe33zvN6rsYyR79Ay9PeQQ/9iokaH4EvvQt2YB8ddLvhIN+SehforgfJGGHoGLQPxFVG08qGfuCTrolEiopwb6uT3guFtzzjD4B/rwcaDLeUrI2JiZk2QkU2YYWevd8y83Hrnnh6FQ3+UmWvwdJNL9OZ+/84Uln8m9/msC9eM738jZF9/4A7/4Wv9l/zKGfLvVV+cReAe6ZCYKgI/xGEcC/HZOoZ/s/aakKIL4045DPSixeQF/vytRT5XlCt4PLLankufQX4zKtU8WfIRqg8/Sd/M9HnLoQQ7wwY7bYsyM+ar/X/7KvTLzh3PxhVcq9VL/bvWNBFHB+gXfJ/B3c9LWT/ykB3xy9wHwA/3oZBWQ75AP81LPqyP5OR9fBPQwYTXnOKDQ76OD4Kur7AT0KRyA5jA0aHABfRZsDBjDOdTAFy6HE9SpN/BHVlqDDfEH90csa80vzxO9KWIzfPEb8ybh/Hv+k33MAzxsL0v89oADzqJkb/zrUu/Jwm9aegA/9cqvUYxfr9Cnu/TGpQelLOQuXJPik1vbQ6wRbqVZ+ylroBa4L1p0ThxGp8zRgnTRDmpTEDPSyCPZVJsGJaEnU6nsnVShhPuAH66KfvoW9+NIcmOXM/GJTTLhDCXYCLoF28rGbmrzOQX9o/3mIxb+tcrVQ+koVQnN9kI3dPZC8KddH4XIULeC/ICsGwTpxxM1XhGH4A+of8Q36d40pMba3Qsc5varU29Mo9oopj59LvOGxJ0OYyNihvG2sqOW9/QZ7Ga6Jb129IvaCLw3gCD/b5fYoTvKtMOtcaekuVR+d8lwOvJZjNzBBmLwlM8C9JTv0gz1rBcPgE0E/CZV3CQc63APOnLH6ktp0gsXUUI3j7Y4cqQc8VwKc2Zcs9Lp7H0feYlogPF7SSxUqo+Pc201kzDiM+1WKO3gM0sMpdTPwPzeS66T4th0xeylCtGskuNHPZsWNKGI+/V7CgUDtPE5D1avv+ot0NB981lJ8W3Rp5UjPjRe+NAFhPmytnVIu7Xi9hXtwCuKvY4k2FrF1VqBfgYd/XhRG9rFwdYGJWqpbHVRoP/iDWli0LPxJgJdmtrxHI8Fa1rQ0auijS/J5hU06hY0BWjDw/SLXr/9wfNBQ9plHn1WPWjV4w8teK5sPVQHdyxBI1YO+VRHCvdMQ9Xzj8Jej7+3k5xL+Uf7uEt6sA/OtmOkT1i92HdRB3SI2RZihduiBR0+p07BHm0lfqtZrSKPjj9p1vBLe2c3fd3d9PX9M/+H9v557c+0t7hpb/MH7f0bf4HubqoAfT1/+18Wh/u8wv2mQ3NZ7L/5rYMz5WDD7zX8fV4j6bfih0+2E5m7K2EF/HXz7+MkVnVgQP+Tb5Xt/vG7iw3o730XVNSHAiWV2/+ZfaJfbP4mvmwJrR/7f80tPqHmWf+T50t/dc8/s+V7zMtgPSqxbn7YbZvudj+sFW1tx216TTZ8hPptwD6raCnkz6tVzK9jvPE6EqTAERU8nZpd+xfnVr/PMagDaoAc+qhuefw9h/8j36D/7TlTBcu8cvqvqam/98dtNlf1ePyRl4amEOOZtI92Giz14vJR5B7agV06c8f97/dqdE5PlRMNkOd/yHXEOKLsP5krkcL/82exoAXuc+UDMglTB7KBva7WrNrOWc4TB8VYtP6VPFlTAToP4m4R27+Qnv/lPNvd/fgvv+lJwBfo0t+GBS+/+t104l57f49fWyzzVut7bi5zwTgQRXqfK+xEi+lNl/fNgdrkptOARj9kDCfljSciq/7i4VV3Qly6R9AZb+KIecU6i1s0A30nykAl1dE7FfYZ1UBCiEQJ8FAXcOXC3h1ovPvMyF9zucwsfG7JvLuAhnsDnhcLHA3AbRRo4Deam9vMQbIo2hvzxhhwnE44i8a9zxA88Da672fTLT/qdt+vbbaJVtqcrlUoQNPhC2gY0OjxNZGoo7NBoMnPoPkYkcMhbj0bnldWeAANMijho0VzensxbKA+LTOIB4Y1Jri7guYCDWoeQKMciY/eMjif8N0z2xC159Nbep85XSRI5d/OIBmI0978OoOUQ0Q4ckHzlDJonDsHd4HLwv7wXODg76CJwd5/dIZluT9ix7t5OU8M51czBs1I3xaNCLEMM9AAe/YI9uuF8y8zmZLi6B38E8UG7GZe+aWJnsA/+aJZq244y64AfR5fxfEPMy6DCQ30AzzPA60ZgoZvhKPRMgNcNLPoxw44MdSt/7UZD/CuU4oMi3Oa0247MyRWe8Mn2g+AB/rCrdrNfPf9T2c8/U+alQnQDtiVEuFlBgb1vgT8PYA/bjM2iNcyc7SY0HSJ/x2PyGGIeqAh7vshNdz3W0vweZ4Fl4sKkOR9JFgblVSoc8EV1Gzhl75oyp42oDkB+Pqcdmta9q/LTPpUiOg9O6qEQrpwc/cPB334pbmeqmVmAZoZ8uFhmaGDhh4Bn3A/xCnvptJfh6wfIb4NaPYBzrf2Aa+AN/Egv/YTrdfc34cA/vxJKoc20EVWohNCY8jMjjQZPk2KN1IvM7Qbvk/XZcZ1e7+Sm7js8KCM/1F0Jikh/twCPcZEqG3kKgdPWv5tJhvxtuPxBL40oG2pxl4PeTHGHR320C3L1puobaJS4iPfNA7l7gs51o7ciLhGzQrOwkQrsOpSyA29K3KyTQ3YysWzYnjWfgoC37VBo+9qeXLKHiMqo4/CGle5Q0cZei/sSK/xpvlg8mzTboS8xAOd8ZiEfIq7yyWzh3DJpdrgMvHXLwxQqYCDlEe92eXDtswHl4joAfY7UNmt6hb0uFRDHFirndRxGXpp+YR2JSIvWVhPYAdNJBFJqAvg6DPl05yx5iwFcUUuNtxGeWHXaNHx3PanFHyVdlHI7de57JVX2pd53w954g9OaSuqjtGUW+O830RKsSYmIXANm6gsECk9UryTJyQY/iZ7IaWcRmKJh5oZyu2h1UeRVYESuxyf6XF4qPrTTOZ45pY7Jj561rID33hRsom8/+e13+395TR+75P/AFf+b9WUv+wdou/vt9c/uBrszXvRQ6+fy/8D+FX9/azh/aw7+Rd9klmjgr11/vixcHT15AJPv7zeP/NG0MLAdba/rFWOZ6redNvQu1a2GqqAv+qc/HjHvQ3EWEhz/nu6B+wxoB0/dGCaCq+tfe6Z75j5E///BmvELPv80Cet/5GKJkrl2uEh9fcMe9BjmsoZVO3oIbWgpwbrVdr7YyWaVM8G6iOhhRM7rGs+6azCVKjnPcferotoyiNPW8JL4Zr6+GVv1k+cp5d89mTcbyfWAn/ylat8fa6EyZdrbZnb/fCX1rYK0tacSKBXWU92qlWN9GmogcXxbtgK0Mui1w3wBGt/fLT3fLVKbc2zHkW0F8Ara6jJ9I3ZGKcmEtAvMtpNKN48QkOkDm21V4VRwWbSgZ5bAQtpSkudoN9PJVT72G4IHMVPePNWSLQhdu3mFoUaDVQ554621t8g75+kwTuo71uI+UE79aiCsStxxLRQn3GuTzGOV9D/rX0IveOAHlJhMLcUUqEuIT5NJryt6tYzC2u3sKdRd8OG+uIJfN4K6CQJX40V1++iNyzthm/7HPJkjtI9Fs+xbc57UyC5eXUryAd+jI6wvilnMXNunpSFQt3TN+2QlRLNJu7BFw7Ucwv6X6geyEYf61AFrI/cHHkp9GrBWY3EBvpk+OjqTpvSIh7l0YYa0B+BNcVCZIqjhhz9C3C/h4ppFluYJ9wtiMAhDSNZI9ozZt5Key2Bj79X0CvSo3nXvr4QHOF9i7d6E7s1cJx6fpxUQN6JI3ag5c9prj6UtUIl4pPsa7sMNKMc7wg/WzthVsBzv+3x1kqPeJdwYicblXDGXdBzbSb0oeAru+qUwzf4m7Ybq5y9XB6jRBy7izriRATaKFzPgJ95L14tsSG7uG0GgfFTcRwMYPGDzGqsOrwrBCgLB4eJ0DLzY7QPRQB98mMnhp3Gw7XKoy4VFIhOpBLfeMVRo7hf3lNp8HGjEkaUNK9OHQwb3Q8H2Q0H3dEi6+AzpF4qFI2xI+bYPjk8eJ2qWb1DfjwA1jvGG5yFQ59aayk32wvgwhc5biuz/tByGDTwcw1aTwk+CU4/SRgtc4JtcVRY+GQF1ziR9El1Ajq95+yPeopDbWoff+6P4jM1gyS9IjXiowiNTUKcVAv/QdgRRzJo8HXRIw6Ysyj4aidEoFj0Atyx0QGNaCiaCjgBaM1LjLcLX3IgJmVmsNIcU9Ktoec0b7QTeZID7zjqaz0bWljCzpxhU4gGYjF8sBB8HDQ9OXausgAXKMr2cvwkPc6Zo8LKF2YviZF5fUmkBT2eAqd1FUOeX7TA8VCTlbl5Am4jJOglqNeIc4WEv35mwTqvHcUyR530sUkgOqPgxch91RT938b6SL/tOZrKQJgKYyN6egRtN0BMRiYtq7KiThqdctukzI7eQEMyKV0ntoYZ+JVTd+vTPh9kvWleFB9deoV+ALyc29tLHYyilutLHNIkk+ZNhP4F4nQprNhOAmx46C2RcRKucJwLWltuVBk9xuz1onvxyVvgyJtGAnZzWLtALXbLXB8UM6TyEeSQTiuOP6tj45TW8nsf88mO3Yr2pkhAw+6P8Qg5CHUooglwvtifJsqbkQYxqrppK/q/ObWgGfNJUImoo8KbuENMirRVzY+jdrwkO9JjelRuKlVRYkOF4/EC4eZ2doM32dw813lkxzxd1aBHk2AcMuDr8LwMeCBwQBIxHjtF6x1A71n6qEEHpdfcdk8U6jmxzW7fNkEcNG+pvQatjWdqQy4z7wj+k8A5rwwPL3VLaW6LTvvRKZHGBrw+C5ueK2lOUE9fuIwgPw3gH2Exe1zZU6quKFY95tqmLevXRIdQ21rSk6AAjeM+7FhzTXB00oE/CUw80ZI3sMGhHXFipN+ZVNDlIRfBt5LHFx5AtfS7GXQay4z3jYXFlCIaZ/04MYOfeahPwo92kFe7GusgC8kHC8YLP+onnp8uKW/c2DdPNf7btLwvTDv1WSHoBVJFdWic///e4//u9x5VAFoRr8fKpgN8vy1yOlS2+w043L/PRVvfSdgWQUwR9I56a362xVt/99u3bPr5t6WX5cw6wB3s2fyGbzd1CHwU1lWArSJD/2Gc/jIX/vvzw//O2P7j8/bf+VdMH9+y5Ye+t9+B3uIEsYd9t1PCugnyxSZX1KqND3nnT6r1IX9Az2QWrMRTHPgO2ZCOtI+Hb+k/F7uzd7w+WiT7p8u/Vtd/uTx3h/hfN6t/yp6frtVh/ZyEz8NHcpoj698Ai5sl4W8sAAA="
}

# ==============================
# GET STAFF FROM API
# ==============================
response = requests.get(url, headers=headers)
staff_list = response.json()

print("Total staff from API:", len(staff_list))

excel_file = "data/staff.xlsx"

# ==============================
# LOAD EXISTING STAFF
# ==============================
if os.path.exists(excel_file):

    existing_df = pd.read_excel(excel_file)

    existing_df.columns = (
        existing_df.columns
        .str.strip()
    )

else:

    existing_df = pd.DataFrame(
        columns=[
            "Lect ID",
            "Staff Name",
            "Email"
        ]
    )

# Existing Lecturer IDs
existing_ids = set(
    existing_df["Lect ID"].astype(str)
)

new_staff = []
existing_staff = 0

# ==============================
# CHECK & ADD NEW STAFF
# ==============================
for staff in staff_list:

    lect_id = str(staff["CODE"]).strip()
    staff_name = staff["FULLNAME"].strip()

    staff_email = staff.get("EMAIL")

    if staff_email:
        staff_email = staff_email.strip()
    else:
        staff_email = ""

    if lect_id in existing_ids:

        existing_staff += 1

    else:

        new_staff.append({
            "Lect ID": lect_id,
            "Staff Name": staff_name,
            "Email": staff_email
        })

        existing_ids.add(lect_id)

# ==============================
# SAVE NEW STAFF
# ==============================
if new_staff:

    new_df = pd.DataFrame(new_staff)

    final_df = pd.concat(
        [
            existing_df,
            new_df
        ],
        ignore_index=True
    )

    final_df.to_excel(
        excel_file,
        index=False
    )

# ==============================
# SUMMARY
# ==============================
print("==============================")
print("STAFF IMPORT COMPLETED")
print("==============================")
print(f"Existing staff skipped : {existing_staff}")
print(f"New staff added        : {len(new_staff)}")
print(f"Total staff in Excel   : {len(existing_df) + len(new_staff)}")