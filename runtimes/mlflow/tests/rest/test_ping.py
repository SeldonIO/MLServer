async def test_invocations(rest_client):
    response = await rest_client.get("/ping")

    assert response.status_code == 200
    assert response.json() == "\n"
