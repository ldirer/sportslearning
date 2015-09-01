/**
 * Created by laurent on 7/10/14.
 */

function get_shot_type_pie_chart (shot_list) {
    var shot_type_count = {};
    $.each(shot_list, function (i, e) {
        shot_type_count[this.shot_type] = (shot_type_count[this.shot_type] || 0) + 1;
    });

    var shot_type_pie_chart = [
        {
            key: "Coups droits",
            y: shot_type_count.F
        },
        {
            key: "Revers",
            y: shot_type_count.B
        }
    ];

    return shot_type_pie_chart;
}
