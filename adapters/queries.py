
ALL_TASKS = """
{
    tasks(lang: en, gameMode: regular) {
        id
        name
    		trader{name, imageLink}
    		map{name}
    		wikiLink
    		taskImageLink
    		minPlayerLevel
            taskRequirements{task{name}}
    		objectives {
				description
				... on TaskObjectiveItem {
					id
					count
					foundInRaid
					items {
					name
					id
					image512pxLink
					wikiLink
					}
					description
				}
				type
				}
    }
}
"""