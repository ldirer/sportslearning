/* global QUnit:false, get_shot_type_pie_chart:false */

QUnit.module("shot_type_count");
QUnit.test("A point with 2 F and 2 B.", function(assert) {
    var shot_list = [
    {
        "start_position_x": 0.530534351145,
        "start_position_y": 0.925430210325,
        "end_position_x": 0.343511450382,
        "end_position_y": 0.286806883365,
        "player": true,
        "shot_type": "S",
        "special_shot": "NULL",
        "timestamp": null
    },
    {
        "start_position_x": 0.259541984733,
        "start_position_y": 0.0726577437859,
        "end_position_x": 0.324427480916,
        "end_position_y": 0.78776290631,
        "player": false,
        "shot_type": "F",
        "special_shot": "NULL",
        "timestamp": null
    },
    {
        "start_position_x": 0.286259541985,
        "start_position_y": 0.938814531549,
        "end_position_x": 0.335877862595,
        "end_position_y": 0.112810707457,
        "player": true,
        "shot_type": "B",
        "special_shot": "NULL",
        "timestamp": null
    },
    {
        "start_position_x": 0.381679389313,
        "start_position_y": 0.0210325047801,
        "end_position_x": 0.343511450382,
        "end_position_y": 0.757170172084,
        "player": false,
        "shot_type": "F",
        "special_shot": "NULL",
        "timestamp": null
    },
    {
        "start_position_x": 0.389312977099,
        "start_position_y": 0.898661567878,
        "end_position_x": 0.248091603053,
        "end_position_y": 0.0841300191205,
        "player": true,
        "shot_type": "B",
        "special_shot": "NULL",
        "timestamp": null
    }
    ];
    var shot_type_pie_chart_ground_truth = [
        {
            key: "Coups droits",
            y: 2
        },
        {
            key: "Revers",
            y: 2
        }
        ];
    assert.deepEqual(get_shot_type_pie_chart(shot_list), shot_type_pie_chart_ground_truth);
});

QUnit.test("With empty shot_list", function(assert) {
    var shot_list_empty = [];
    var shot_type_pie_chart_ground_truth_empty = [
        {
            key: "Coups droits",
            y: undefined
        },
        {
            key: "Revers",
            y: undefined
        }
        ];
    assert.deepEqual(get_shot_type_pie_chart(shot_list_empty), shot_type_pie_chart_ground_truth_empty);
});