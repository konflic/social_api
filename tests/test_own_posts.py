import datetime


def test_create_post(logged_in_session, host):
    response = logged_in_session.get(f"{host}/posts")
    response.raise_for_status()

    posts_before_creation = response.json()
    now = datetime.datetime.now()

    put_response = logged_in_session.put(
        f"{host}/post",
        json={
            "title": "title fof test",
            "content": f"stringstringstringstringstringstringstringstringst {now}",
        },
    )

    put_response.raise_for_status()

    response = logged_in_session.get(f"{host}/posts")
    response.raise_for_status()
    posts_after_creation = response.json()

    assert (
        len(posts_before_creation) == len(posts_after_creation) - 1
    ), "New post was not created"


def test_edit_own_post(logged_in_session, host):
    put_response = logged_in_session.put(
        f"{host}/post",
        json={
            "title": "title fof test",
            "content": "stringstringstringstringstringstringstringstringst",
        },
    )

    post_id = put_response.json().get("id")

    edit_response = logged_in_session.patch(
        f"{host}/post/{post_id}",
        json={
            "title": "new title",
            "content": "new content stringstringstringstringstringstringstringstringst",
        },
    )

    edit_response.raise_for_status()

    edited_post_response = logged_in_session.get(f"{host}/post/{post_id}")
    edited_post_response.raise_for_status()
    post_data = edited_post_response.json().get("Post")

    assert "new title" in post_data.get(
        "title"
    ), "Title of post was not changed after editing"
    assert "new content" in post_data.get(
        "content"
    ), "Content of post was not changed after editing"


def test_delete_own_post(logged_in_session, host):
    put_response = logged_in_session.put(
        f"{host}/post",
        json={
            "title": "title fof test",
            "content": "stringstringstringstringstringstringstringstringst",
        },
    )

    post_id = put_response.json().get("id")

    delete_response = logged_in_session.delete(f"{host}/post/{post_id}")
    delete_response.raise_for_status()

    check_deleted_post = logged_in_session.get(f"{host}/post/{post_id}")
    assert (
        check_deleted_post.status_code == 404
    ), f"Post {post_id} was not deleted, or status is not 404"


def test_like_own_post(logged_in_session, host):
    put_response = logged_in_session.put(
        f"{host}/post",
        json={
            "title": "title fof test",
            "content": "stringstringstringstringstringstringstringstringst",
        },
    )

    post_id = put_response.json().get("id")

    like_response = logged_in_session.post(f"{host}/post/{post_id}/like")

    assert like_response.status_code == 400, "Wrong status on own like of own post"
    assert (
        like_response.json().get("detail") == "you cant like own post"
    ), "Wrong status on own like of own post"


def test_dislike_own_post(logged_in_session, host):
    put_response = logged_in_session.put(
        f"{host}/post",
        json={
            "title": "title fof test",
            "content": "stringstringstringstringstringstringstringstringst",
        },
    )

    post_id = put_response.json().get("id")

    dislike_response = logged_in_session.post(f"{host}/post/{post_id}/like")

    assert (
        dislike_response.status_code == 400
    ), "Wrong status on own dislike of own post"
    assert (
        dislike_response.json().get("detail") == "you cant like own post"
    ), "Wrong status on own dislike of own post"
