def recalculate_student_plan_progress_by_student_plan(student_plan, user_pk):
    topic_plans = []
    for subject_plan in student_plan.subject_plan.all():
        topic_plans += subject_plan.topic_plan.filter(topic__is_mid_control=False)
    percent_for_one_topic = 100.0 / len(topic_plans) if len(topic_plans) > 0 else 0.0
    single_plan_progress = {
        0.0: 0,
        0.5: percent_for_one_topic/6.0,
        1: percent_for_one_topic/3.0
    }

    progress = 0.0
    for topic_plan in topic_plans:
        progress += single_plan_progress[topic_plan.tutorial]
        progress += single_plan_progress[topic_plan.class_work]
        progress += single_plan_progress[topic_plan.home_work]
    student_plan.progress = progress
    student_plan.save(user_pk=user_pk)
