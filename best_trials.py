import optuna
study = optuna.create_study(study_name='pistonball18', storage='mysql://root:dummy@10.128.0.28/pistonball18', load_if_exists=True, direction="maximize")
print(study.best_trial)
for i in study.trials:
    print(i.value)

# print(study.trials)


# trial = study.best_trial

# optuna.study.StudySummary(study)
# summary = optuna.study.get_all_study_summaries('mysql://root:dummy@10.128.0.28/pistonball18')

# for i in study.trials:
#     print(i.value)
