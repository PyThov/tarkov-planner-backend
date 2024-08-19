
ALL_TASKS = """
{
    tasks(lang: en, gameMode: regular) {
        id
        name
        kappaRequired
    		trader
            {
            	name,
                imageLink
            }
    		map {
            	name,
            	wiki
            }
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