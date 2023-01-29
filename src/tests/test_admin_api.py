from .conftest import async_sessionmaker

get_headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNYNVZwY1JCcjFWUmVBa2pFYjl2My13R0luVSJ9.eyJhdWQiOiJiNTNhNzUyMC02YjIyLTQzYzctYjIxOC04MzBkZTNmODBiNDIiLCJleHAiOjE2NzQ5ODY2NzYsImlhdCI6MTY3NDk4MzA3NiwiaXNzIjoibWF4aW1sLmNvbSIsInN1YiI6IjllMWU5Y2FmLWU0NGQtNGIwZi1iZTFlLTcxMTAwZmI3MDkyMCIsImp0aSI6IjI5MjlhYjk3LWUyOWUtNDVkZi05NjljLWNhMGQ5MTIwOTI5NCIsImF1dGhlbnRpY2F0aW9uVHlwZSI6IlBBU1NXT1JEIiwiZW1haWwiOiJudWNsZXVzQG1heGltbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoibnVjbGV1c0BtYXhpbWwuY29tIiwiYXBwbGljYXRpb25JZCI6ImI1M2E3NTIwLTZiMjItNDNjNy1iMjE4LTgzMGRlM2Y4MGI0MiIsInJvbGVzIjpbIkFQSV9LRVlfR0xPQkFMX0FETUlOSVNUUkFUSU9OIiwiQVBJX0tFWV9TRUxGX0FETUlOSVNUUkFUSU9OIiwiR0xPQkFMX0pPQl9BRE1JTklTVFJBVElPTiIsIkdMT0JBTF9KT0JfRVhFQ1VUSU9OIiwiR0xPQkFMX1VTRVJfQURNSU5JU1RSQVRJT04iLCJHTE9CQUxfVVNFUl9PTkJPQVJESU5HIiwiR0xPQkFMX1dFQkhPT0tfQURNSU5JU1RSQVRJT04iLCJKT0JfUk9MRVNfQURNSU5JU1RSQVRJT04iLCJKT0JfUk9MRVNfVklFV0lORyIsIk1BTkFHRV9BU1NFVFMiLCJNQU5BR0VfR1VJREVTIiwiTUFOQUdFX01BU1RFUl9EQVRBIiwiTUFOQUdFX01BU1RFUl9TQ0hFTUEiLCJTSVRFX0FETUlOSVNUUkFUSU9OIiwiU0lURV9MRVZFTF9KT0JfQURNSU5JU1RSQVRJT04iLCJTSVRFX0xFVkVMX0pPQl9FWEVDVVRJT04iLCJTSVRFX0xFVkVMX1VTRVJfQURNSU5JU1RSQVRJT04iLCJTSVRFX0xFVkVMX1VTRVJfT05CT0FSRElORyIsIlNZU1RFTV9BRE1JTklTVFJBVElPTiIsIlRFTVBMQVRFX0FETUlOIiwiVEVNUExBVEVfVklFV0VSIiwiVklFV19BTExfSk9CU19BTkRfQUNUSU9OUyIsIlZJRVdfQU5BTFlUSUNTIiwiVklFV19BU1NFVFMiLCJWSUVXX0dVSURFUyIsIlZJRVdfTUFTVEVSUyJdLCJmdWxsTmFtZSI6Ik51Y2xldXMiLCJ1c2VySWQiOiI5ZTFlOWNhZi1lNDRkLTRiMGYtYmUxZS03MTEwMGZiNzA5MjAiLCJ0ZW5hbnRJZCI6IjZiYjY2Mzc2LTU5YTAtNDgxYi1iYjE4LWYzNmQzOGU5MjM2MCIsInVzZXJuYW1lIjoibnVjbGV1c0BtYXhpbWwuY29tIn0.zQRQbQcGWksnWtMrI_8SIirQ9MQIcatylQCc-n9T8i71uvDtaGQwUmsUYA1B0pz-tqgpPy1M-e69y4apxVZ5vST5DzT3iuzu6j6Bub0yECguwyTf3ZuBEKcZ3xwl2WdkqMjLKAeqEgWNPAbvRrM3OMOjwxfXWplM4EyFfIJZKTOyHcvyegRFVEADYRWpnvdrAjG0wk0XBI4e8QQAskrOuwKlNx5jPdsMy1XLDyou4OgnsIpdmEfLhPgcfktBgBN1auJ9007oFGYujx2gj3GoqkyzS-aVhN_QY5iwkwHn6OfZBkmVgMa-cZpqFJnl20pSkWAD6yqMMOV0h4S7jkzKlw"
}
post_headers = {
    **get_headers,
    "Content-Type": "application/json"
}

class TestTagType:
    def test_create(self, client):
        response = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "Tenant"
    
    def test_get(self, client):
        client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        client.post("/admin/tagtypes", json={
            "name": "Application"
        }, headers=post_headers)
        response = client.get("/admin/tagtypes", headers=get_headers)
        assert response.status_code == 200
        content = response.json()
        assert len(content) == 2

class TestTagValue:
    def test_create(self, client):
        response = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        content = response.json()
        res1 = client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "dev-nucleus"
        }, headers=post_headers)
        print(res1.content)
        assert res1.status_code == 200
        cont1 = res1.json()
        assert cont1["value"] == "dev-nucleus"
        assert cont1["tag_type"]["id"] == content["id"]
        assert cont1["tag_type"]["name"] == content["name"]
        res2 = client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "stag-nucleus"
        }, headers=post_headers)
        assert res2.status_code == 200
        cont2 = res2.json()
        assert cont2["value"] == "stag-nucleus"
        assert cont2["tag_type"]["id"] == content["id"]
        assert cont2["tag_type"]["name"] == content["name"]
        res3 = client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "prod-nucleus"
        }, headers=post_headers)
        assert res3.status_code == 200
        cont3 = res3.json()
        assert cont3["value"] == "prod-nucleus"
        assert cont3["tag_type"]["id"] == content["id"]
        assert cont3["tag_type"]["name"] == content["name"]
    
    def test_get(self, client):
        response = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        content = response.json()
        client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "dev-nucleus"
        }, headers=post_headers)
        client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "stag-nucleus"
        }, headers=post_headers)
        client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "prod-nucleus"
        }, headers=post_headers)
        response = client.get("/admin/tagvalues", headers=get_headers)
        assert response.status_code == 200
        content = response.json()
        assert len(content) == 3

class TestEnvironment:
    def test_create(self, client):
        response = client.post("/admin/environments", json={
            "name": "Development"
        }, headers=post_headers)
        assert response.status_code == 200
        content = response.json()
        assert content["name"] == "Development"
    
    def test_get(self, client):
        client.post("/admin/environments", json={
            "name": "Development"
        }, headers=post_headers)
        client.post("/admin/environments", json={
            "name": "Staging"
        }, headers=post_headers)
        client.post("/admin/environments", json={
            "name": "Production"
        }, headers=post_headers)
        response = client.get("/admin/environments", headers=get_headers)
        assert response.status_code == 200
        content = response.json()
        assert len(content) == 3

class TestFeatureFlag:
    def test_create(self, client):
        res0 = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        content = res0.json()
        res1 = client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "dev-nucleus"
        }, headers=post_headers)
        content = res1.json()
        res2 = client.post("/admin/featureflags", json={
            "name": "Flag 1",
            "description": "The first flag",
            "tags": [content["id"]]
        }, headers=post_headers)
        # print(res2.content)
        assert res2.status_code == 200
        content = res2.json()
        assert content["name"] == "Flag 1"
        assert content["description"] == "The first flag"
        assert len(content["tags"]) == 1
        assert content["tags"][0]["value"] == "dev-nucleus"
        assert content["tags"][0]["tag_type"]["name"] == "Tenant"

    def test_update(self, client):
        res0 = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        content = res0.json()
        tag_type_id = content["id"]
        res1 = client.post("/admin/tagvalues", json={
            "tag_type": tag_type_id,
            "value": "dev-nucleus"
        }, headers=post_headers)
        content = res1.json()
        tag_value_id1 = content["id"]
        res2 = client.post("/admin/featureflags", json={
            "name": "Flag 1",
            "description": "The first flag",
            "tags": [tag_value_id1]
        }, headers=post_headers)
        feature_flag = res2.json()

        res3 = client.post("/admin/tagvalues", json={
            "tag_type": tag_type_id,
            "value": "stag-nucleus"
        }, headers=post_headers)
        content = res3.json()
        tag_value_id2 = content["id"]

        res4 = client.patch(f"/admin/featureflags/{feature_flag['id']}", json={
            "name": "Flag 1 - updated",
            "description": "The first flag - updated",
            "tags": [tag_value_id2]
        }, headers=post_headers)

        # print(res2.content)
        assert res4.status_code == 200
        content = res4.json()
        assert content["name"] == "Flag 1 - updated"
        assert content["description"] == "The first flag - updated"
        assert len(content["tags"]) == 1
        assert content["tags"][0]["value"] == "stag-nucleus"
        assert content["tags"][0]["tag_type"]["name"] == "Tenant"
    
    def test_get(self, client):
        res0 = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        content = res0.json()
        res1 = client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "dev-nucleus"
        }, headers=post_headers)
        content = res1.json()
        res2 = client.post("/admin/featureflags", json={
            "name": "Flag 1",
            "description": "The first flag",
            "tags": [content["id"]]
        }, headers=post_headers)
        res3 = client.post("/admin/featureflags", json={
            "name": "Flag 2",
            "description": "The second flag",
            "tags": [content["id"]]
        }, headers=post_headers)
        res4 = client.post("/admin/featureflags", json={
            "name": "Flag 3",
            "description": "The third flag",
            "tags": [content["id"]]
        }, headers=post_headers)
        res5 = client.get("/admin/featureflags", headers=get_headers)
        # print(res2.content)
        assert res5.status_code == 200
        content = res5.json()
        assert len(content) == 3
        assert content[0]["name"] == "Flag 1"
        assert content[0]["description"] == "The first flag"
        assert len(content[0]["tags"]) == 1
        assert content[0]["tags"][0]["value"] == "dev-nucleus"
        assert content[0]["tags"][0]["tag_type"]["name"] == "Tenant"

class TestFeatureFlagValue:
    def test_update(self, client):
        res0 = client.post("/admin/tagtypes", json={
            "name": "Tenant"
        }, headers=post_headers)
        content = res0.json()
        res1 = client.post("/admin/tagvalues", json={
            "tag_type": content["id"],
            "value": "dev-nucleus"
        }, headers=post_headers)
        content = res1.json()
        res2 = client.post("/admin/featureflags", json={
            "name": "Flag 1",
            "description": "The first flag",
            "tags": [content["id"]]
        }, headers=post_headers)
        feature_flag = res2.json()
        res3 = client.post("/admin/environments", json={
            "name": "development"
        }, headers=post_headers)
        environment = res3.json()
        res4 = client.patch(f"/admin/featureflags/{feature_flag['id']}/value", params={"environment_id": environment["id"]}, json={
            "enabled": True,
            "rollout_percent": 100
        }, headers=post_headers)
        content = res4.json()
        assert res4.status_code == 200
        assert content["name"] == "Flag 1"
        assert content["description"] == "The first flag"
        assert len(content["tags"]) == 1
        assert content["tags"][0]["value"] == "dev-nucleus"
        assert content["tags"][0]["tag_type"]["name"] == "Tenant"
        assert len(content["values"]) == 1
        assert content["values"][0]["enabled"] == True
        assert content["values"][0]["rollout_percent"] == 100
        assert content["values"][0]["environment"]["name"] == "development"
