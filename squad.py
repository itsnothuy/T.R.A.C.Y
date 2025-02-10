from datasets import load_dataset
squad = load_dataset("squad")
nq = load_dataset("natural_questions")
hotpot = load_dataset("hotpot_qa", "fullwiki")
trivia = load_dataset("trivia_qa", "unfiltered")
