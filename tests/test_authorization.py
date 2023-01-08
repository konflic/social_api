def test_main(session, host):
    response = session.get(host)
    response.raise_for_status()


# TODO: Здень нужно покрыть сценарии регистрации нового пользователя
