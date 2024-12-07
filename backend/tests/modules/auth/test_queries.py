import pytest

from daytistics.graphql import schema
from tests.factories import ModernUserFactory


def test_user_query(session):
    user = ModernUserFactory.build()
    session.add(user)
    session.commit()
    session.refresh(user)

    query = f"""
        query {{
            user(id: {user.id}) {{
                id
                email
            }}
        }}
    """

    result = schema.execute_sync(query, context_value={"session": session})
    assert not result.errors
    assert result.data == {
        "user": {
            "id": user.id,
            "email": user.email,
        }
    }
