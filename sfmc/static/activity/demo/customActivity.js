define([
    '../../postmonger'
], function(
    Postmonger
) {
    'use strict';

    var connection = new Postmonger.Session();
    var payload = {};
    var steps = [ // initialize to the same value as what's set in config.json for consistency
        { "label": "Step 1", "key": "step1" },
        { "label": "Step 2", "key": "step2" }
    ];
    var currentStep = steps[0].key;

    $(window).ready(onRender);

    connection.on('initActivity', initialize);
    connection.on('requestedTokens', onGetTokens);
    connection.on('requestedEndpoints', onGetEndpoints);

    connection.on('clickedNext', onClickedNext);
    connection.on('clickedBack', onClickedBack);
    connection.on('gotoStep', onGotoStep);

    function onRender() {
        // JB will respond the first time 'ready' is called with 'initActivity'

        $('#loading').show()
        $('.step').hide();
        connection.trigger('updateButton', {
            button: 'next',
            enabled: false
        });

        connection.trigger('ready');

        connection.trigger('requestTokens');
        connection.trigger('requestEndpoints');
    }

    function initialize (data) {
        if (data) {
            payload = data;
        }

        var input1;
        var input2
        var hasInArguments = Boolean(
            payload['arguments'] &&
            payload['arguments'].execute &&
            payload['arguments'].execute.inArguments &&
            payload['arguments'].execute.inArguments.length > 0
        );

        var inArguments = hasInArguments ? payload['arguments'].execute.inArguments : {};

        $.each(inArguments, function(index, inArgument) {
            $.each(inArgument, function(key, val) {
                if (key === 'input1') {
                    input1 = val;
                } else if (key === 'input2') {
                    input2 = val;
                }
            });
        });

        $('#input-1').val(input1);
        $('#input-2').val(input2);
    }

    var access_token = null
    var endpoint = null
    function onGetTokens (tokens) {
        console.log(tokens)
        $('#token').html('token: ' + tokens.token + '  fuel2token:'+tokens.fuel2token)
        access_token = tokens.fuel2token
        getTokenContext()
    }

    function onGetEndpoints (endpoints) {
        $('#baseUrl').html('endpoints:'+endpoints.restHost)
        endpoint = endpoints.restHost
    }

    var org_id = null
    function getTokenContext() {
        $.ajax({
            url: '/tokenContext/',
            type: 'GET',
            data: {
                'token':access_token
            }
        }).done(function(result){
            $('#loading').hide()
            $('#step1').show()
            connection.trigger('updateButton', {
                button: 'next',
                enabled: true
            });
            org_id = result.organization.id
        }) 
    }

    function onClickedNext () {
        if (currentStep.key === 'step2' ) {
            save();
        } else {
            connection.trigger('nextStep');
        }
    }

    function onClickedBack () {
        connection.trigger('prevStep');
    }

    function onGotoStep (step) {
        showStep(step);
        connection.trigger('ready');
    }

    function showStep(step, stepIndex) {
        if (org_id == null) return
            
        if (stepIndex && !step) {
            step = steps[stepIndex-1];
        }

        currentStep = step;

        $('.step').hide();

        switch(currentStep.key) {
            case 'step1':
                $('#step1').show();
                connection.trigger('updateButton', {
                    button: 'next',
                    enabled: true
                });
                connection.trigger('updateButton', {
                    button: 'back',
                    visible: false
                });
                break;
            case 'step2':
                $('#step2').show();
                connection.trigger('updateButton', {
                    button: 'back',
                    visible: true
                });
                connection.trigger('updateButton', {
                    button: 'next',
                    text: 'next',
                    visible: true
                });
                break;
        }
    }

    function save() {
        // 'payload' is initialized on 'initActivity' above.
        // Journey Builder sends an initial payload with defaults
        // set by this activity's config.json file.  Any property
        // may be overridden as desired.
        payload.name = "First Payload";

        payload['arguments'].execute.inArguments = [{ "input1": $('#input-1').val(), "input2": $('#input-2').val(), "org_id": org_id }];

        payload['metaData'].isConfigured = true;

        connection.trigger('updateActivity', payload);
    }

});