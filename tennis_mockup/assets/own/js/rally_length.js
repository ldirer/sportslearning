/**
 * Created by laurent on 7/28/14.
 */

function rally_length (point) {
    // Brute Force, we don't need to check all points for shot_type: once we
    // have a non-serve, we will not encounter any more serve.
    var shot_count = 1;
    $.each(point.shots, function(i, e) {
        if(this.shot_type !== 'S') {
            shot_count = shot_count + 1;
        }
    });
    return shot_count;
}