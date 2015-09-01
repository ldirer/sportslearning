/**
 * Created by laurent on 7/28/14.
 */

QUnit.module('rally_length');
QUnit.test("A point with one serve.", function(assert) {
    var point = {
            "py/object": "TennisPoint.TennisPoint",
            "_conclusion": "Unforced",
            "shots": [
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855625.100267,
                    "shot_type": "S",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.5305343511450382,
                        "y": 0.9254302103250478
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.3435114503816794,
                        "y": 0.28680688336520077
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855666.256413,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.2595419847328244,
                        "y": 0.07265774378585087
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.3244274809160305,
                        "y": 0.7877629063097514
                    },
                    "_special_shot": null,
                    "_player": 0
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855670.276186,
                    "shot_type": "B",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.2862595419847328,
                        "y": 0.9388145315487572
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.33587786259541985,
                        "y": 0.11281070745697896
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855672.708362,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.3816793893129771,
                        "y": 0.021032504780114723
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.3435114503816794,
                        "y": 0.7571701720841301
                    },
                    "_special_shot": null,
                    "_player": 0
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855678.205891,
                    "shot_type": "B",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.3893129770992366,
                        "y": 0.8986615678776291
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.2480916030534351,
                        "y": 0.0841300191204589
                    },
                    "_special_shot": null,
                    "_player": 1
                }
            ],
            "_player_scoring": 0,
            "_score": {
                "py/object": "Score.Score",
                "_games": [
                    0,
                    0
                ],
                "_points": [
                    1,
                    0
                ],
                "_sets": [
                    0,
                    0
                ]
            }
        };
    var rally_length_ground_truth = 5;
    assert.equal(rally_length(point), rally_length_ground_truth);
});

QUnit.test("With empty shot_list", function(assert) {
    var point_empty = {
        "py/object": "TennisPoint.TennisPoint",
        "_conclusion": "Unforced",
        "shots":[],
        "_player_scoring": 0,
            "_score": {
                "py/object": "Score.Score",
                "_games": [
                    0,
                    0
                ],
                "_points": [
                    1,
                    0
                ],
                "_sets": [
                    0,
                    0
                ]
            }
    };
    var rally_length_ground_truth_empty = 1;
    assert.equal(rally_length(point_empty), rally_length_ground_truth_empty);
});


QUnit.test("With 2 serves", function(assert) {
            var point = {
                "py/object": "TennisPoint.TennisPoint",
                "_conclusion": "Winner",
                "shots": [
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855713.212378,
                    "shot_type": "S",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.44656488549618323,
                        "y": 0.9235181644359465
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.6679389312977099,
                        "y": 0.5047801147227533
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855733.070325,
                    "shot_type": "S",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.44656488549618323,
                        "y": 0.9235181644359465
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.5954198473282443,
                        "y": 0.3135755258126195
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855737.102259,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.7099236641221374,
                        "y": 0.0841300191204589
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.48091603053435117,
                        "y": 0.6730401529636711
                    },
                    "_special_shot": null,
                    "_player": 0
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855741.196287,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.42366412213740456,
                        "y": 0.9311663479923518
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.3816793893129771,
                        "y": 0.2294455066921606
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855769.277302,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.3053435114503817,
                        "y": 0.06692160611854685
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.6641221374045801,
                        "y": 0.7533460803059273
                    },
                    "_special_shot": null,
                    "_player": 0
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855773.694023,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.7709923664122137,
                        "y": 0.9464627151051626
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.7137404580152672,
                        "y": 0.15487571701720843
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855781.380423,
                    "shot_type": "B",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.7213740458015268,
                        "y": 0.0497131931166348
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.46946564885496184,
                        "y": 0.7151051625239006
                    },
                    "_special_shot": null,
                    "_player": 0
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855786.17236,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.33587786259541985,
                        "y": 0.9082217973231358
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.2824427480916031,
                        "y": 0.1682600382409178
                    },
                    "_special_shot": null,
                    "_player": 1
                },
                {
                    "py/object": "TennisShot.TennisShot",
                    "_timestamp": 1403855794.87776,
                    "shot_type": "F",
                    "_shot_start_position": {
                        "py/object": "point.Point",
                        "x": 0.26717557251908397,
                        "y": 0.0497131931166348
                    },
                    "_shot_end_position": {
                        "py/object": "point.Point",
                        "x": 0.25572519083969464,
                        "y": 0.8011472275334608
                    },
                    "_special_shot": null,
                    "_player": 0
                }
            ],
            "_player_scoring": 0,
            "_score": {
                "py/object": "Score.Score",
                "_games": [
                    0,
                    0
                ],
                "_points": [
                    2,
                    0
                ],
                "_sets": [
                    0,
                    0
                ]
            }
        };
        var rally_length_ground_truth = 8;
        assert.equal(rally_length(point), rally_length_ground_truth);
});