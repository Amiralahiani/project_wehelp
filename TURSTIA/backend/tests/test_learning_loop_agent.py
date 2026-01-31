# ======================================
# Test Learning Loop Agent
# ======================================

from backend.agents.learning_loop_agent import LearningLoopAgent


TEST_CASE_ID = "NEW-1107"


def test_learning_loop_update():
    agent = LearningLoopAgent()

    print("\n--- Learning Loop Test ---")

    result = agent.run(
        case_id=TEST_CASE_ID,
        outcome="DEFAULT",
        loss_amount=1200
    )

    print("Result:", result)

    assert result["status"] in {"UPDATED", "NOT_FOUND"}

    if result["status"] == "UPDATED":
        assert result["payload_update"]["default"] is True
        assert result["payload_update"]["loss_amount"] == 1200

        print("✅ LearningLoopAgent test passed (payload updated)")
    else:
        print("⚠️ Case not found in Qdrant — check case_id")


if __name__ == "__main__":
    test_learning_loop_update()
