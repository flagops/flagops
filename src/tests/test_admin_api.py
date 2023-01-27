from .conftest import async_sessionmaker

get_headers = {
    "X-Tenant-Id": "6e58d992-1069-46d4-bc10-b79cab5716ea"
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
