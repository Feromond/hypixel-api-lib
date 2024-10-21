from hypixel_api_lib.Skills import Skills

skills_manager = Skills()

farming_skill = skills_manager.get_skill("Farming")

print(f"Skill Name: {farming_skill.name}")
print(f"Skill Description: {farming_skill.description}")
print(f"Max Level: {farming_skill.max_level}")

farming_level_10 = farming_skill.get_level(10)
print(f"Level 10 Unlocks: {farming_level_10.unlocks}")

skills_with_max_level_60 = skills_manager.get_skills_by_max_level(60)
print(f"Skills with Max Level 60: {list(skills_with_max_level_60.keys())}")


skill_names = skills_manager.list_skill_names()
print(f"Available Skills: {skill_names}")