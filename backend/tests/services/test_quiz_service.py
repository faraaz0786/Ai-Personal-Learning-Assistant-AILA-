from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from core.exceptions import AppError
from schemas.learn import QuizQuestion
from services.quiz_service import QuizService


def _make_quiz_model(topic_id, questions, session_id):
    model = MagicMock()
    model.id = uuid4()
    model.topic_id = topic_id
    model.questions = [q.model_dump() for q in questions]
    model.question_count = len(questions)
    model.difficulty = "medium"
    return model


def _make_topic_model(topic_id, session_id):
    model = MagicMock()
    model.id = topic_id
    model.session_id = session_id
    return model


def _make_attempt_model(quiz_id, session_id, answers, score, max_score, percentage):
    model = MagicMock()
    model.id = uuid4()
    model.quiz_id = quiz_id
    model.session_id = session_id
    model.answers = answers
    model.score = score
    model.max_score = max_score
    model.percentage = percentage
    return model


SAMPLE_QUESTIONS = [
    QuizQuestion(
        id=1,
        question="What is photosynthesis in basic biology terms?",
        options=["A plant energy process", "A rock cycle stage", "A cloud type", "A force law"],
        correct_index=0,
        explanation="Photosynthesis is the process plants use to make usable energy.",
    ),
    QuizQuestion(
        id=2,
        question="Which input is used during photosynthesis by plants?",
        options=["Carbon dioxide", "Plastic", "Copper", "Helium"],
        correct_index=0,
        explanation="Plants use carbon dioxide, water, and sunlight during photosynthesis.",
    ),
]


@pytest.mark.asyncio
async def test_quiz_service_creates_and_scores_quiz() -> None:
    topic_id = uuid4()
    session_id = str(uuid4())

    quiz_model = _make_quiz_model(topic_id, SAMPLE_QUESTIONS, session_id)
    topic_model = _make_topic_model(topic_id, session_id)
    attempt_model = _make_attempt_model(quiz_model.id, session_id, [0, 1], 1, 2, 50.0)

    quiz_repo = MagicMock()
    quiz_repo.create = AsyncMock(return_value=quiz_model)
    quiz_repo.get_by_id = AsyncMock(return_value=quiz_model)

    attempt_repo = MagicMock()
    attempt_repo.create = AsyncMock(return_value=attempt_model)

    topic_repo = MagicMock()
    topic_repo.get_by_id = AsyncMock(return_value=topic_model)

    service = QuizService(quiz_repo=quiz_repo, attempt_repo=attempt_repo, topic_repo=topic_repo)

    quiz = await service.create_quiz(
        topic_id=topic_id,
        expected_count=2,
        session_id=session_id,
        questions=SAMPLE_QUESTIONS,
    )

    attempt = await service.submit_attempt(quiz.quiz_id, [0, 1], session_id)

    assert attempt.score == 1
    assert attempt.max_score == 2
    assert attempt.results[0].correct is True
    assert attempt.results[1].correct is False


@pytest.mark.asyncio
async def test_quiz_service_rejects_answer_count_mismatch() -> None:
    topic_id = uuid4()
    session_id = str(uuid4())

    single_question = [SAMPLE_QUESTIONS[0]]
    quiz_model = _make_quiz_model(topic_id, single_question, session_id)
    topic_model = _make_topic_model(topic_id, session_id)

    quiz_repo = MagicMock()
    quiz_repo.create = AsyncMock(return_value=quiz_model)
    quiz_repo.get_by_id = AsyncMock(return_value=quiz_model)

    attempt_repo = MagicMock()
    topic_repo = MagicMock()
    topic_repo.get_by_id = AsyncMock(return_value=topic_model)

    service = QuizService(quiz_repo=quiz_repo, attempt_repo=attempt_repo, topic_repo=topic_repo)

    quiz = await service.create_quiz(
        topic_id=topic_id,
        expected_count=1,
        session_id=session_id,
        questions=single_question,
    )

    with pytest.raises(AppError) as exc:
        await service.submit_attempt(quiz.quiz_id, [0, 1], session_id)

    assert exc.value.code == "ANSWER_COUNT_MISMATCH"
