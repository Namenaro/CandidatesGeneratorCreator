from candidates_selection.step_constructor import StepsLibrary
from candidates_selection.track import Track, create_track_from_json


from typing import List, Dict, Any
from candidates_selection.multitrack_results import MultitrackResult



class MultiTrack:
    def __init__(self, tracks_names:List[str]=None, tracks:List[Track]=None):
        self.tracks_names = tracks_names
        self.tracks = tracks

    def run(self, signal, left, right)->MultitrackResult:
        result = MultitrackResult()
        for i in range(len(self.tracks)):
            track = self.tracks[i]
            track_name = self.tracks_names[i]

            # запускаем трек на выполнение (это обязательно перед запросом результатов, ведь пока их нет или они старые!)
            track.fill_results(signal, left=left, right=right)

            result.add_track_candidates(track_name, track_candidates=track.get_candidates_coords())
            result.add_track_detailed_history(track_name, steps_results=track.get_history_signal_changes())
        return result




def create_multitrack_from_json(data:Dict[str, Any], step_library:StepsLibrary) -> MultiTrack:
    tracks_names = []
    tracks = []

    for track_name, track_data in data.items():
        track = create_track_from_json(data=track_data, step_library=step_library)

        tracks_names.append(track_name)
        tracks.append(track)

    multitrack = MultiTrack(tracks_names=tracks_names, tracks=tracks)
    return multitrack




