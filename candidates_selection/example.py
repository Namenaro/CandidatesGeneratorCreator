from paths import PATH_TO_MULTITRACKS
from multitrack_results import MultitrackResult
from multitrack import MultiTrack, create_multitrack_from_json
from step_constructor import StepsLibrary
from pathlib import Path

import json5 as json

if __name__ == "__main__":
    file_path = Path(PATH_TO_MULTITRACKS + "\\test_multi.json")
    step_library = StepsLibrary()
    with open(file_path, 'r') as f:
        existing_data = json.load(f)

        first_multitack_name = list(existing_data.keys())[0]
        multitrack_data = existing_data[first_multitack_name]

        multitrack = create_multitrack_from_json(step_library=step_library, data=multitrack_data)
        results = multitrack.run(signal = [0, 1, 2, 3,4,5.6, 7, 8, 9], left=2/500, right=6/500)
        candidates = results.get_all_candidates()
        history_signals_change = results.get_track_detailed_history("track1")
        for step_signal in history_signals_change:
            print(step_signal)

        print("коордитаны ", str(candidates))


