from storycast.models import ScenePlan, StoryBlueprint


def test_blueprint_normalizes_duration_to_target() -> None:
    blueprint = StoryBlueprint(
        title="Stellar Exit",
        topic="the death of a star",
        logline="A star lives fast and dies loud.",
        narrator_brief="Warm documentary narrator",
        visual_style_bible="Grand cosmic photography",
        music_direction="Slow-burn orchestral",
        estimated_total_seconds=58,
        scenes=[
            ScenePlan(index=1, title="Spark", duration_seconds=9, narration="One", visual_prompt="A", motion_prompt="B", mood="curious"),
            ScenePlan(index=2, title="Pressure", duration_seconds=9, narration="Two", visual_prompt="A", motion_prompt="B", mood="tense"),
            ScenePlan(index=3, title="Ignition", duration_seconds=10, narration="Three", visual_prompt="A", motion_prompt="B", mood="electric"),
            ScenePlan(index=4, title="Burn", duration_seconds=10, narration="Four", visual_prompt="A", motion_prompt="B", mood="majestic"),
            ScenePlan(index=5, title="Collapse", duration_seconds=10, narration="Five", visual_prompt="A", motion_prompt="B", mood="violent"),
            ScenePlan(index=6, title="Echo", duration_seconds=10, narration="Six", visual_prompt="A", motion_prompt="B", mood="awe"),
        ],
    )

    normalized = blueprint.normalized(60)

    assert sum(scene.duration_seconds for scene in normalized.scenes) == 60
