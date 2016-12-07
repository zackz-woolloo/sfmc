define([
    'postmonger'
], function(
    Postmonger
) {
    'use strict';

    var connection = new Postmonger.Session();
    var payload = {};
    var lastStepEnabled = false;
    var steps = [ // initialize to the same value as what's set in config.json for consistency
        { "key": "step1", "label": "Step 1" }
    ];
    var currentStep = steps[0].key;

    $(window).ready(onRender);

    connection.on('initEvent', initialize);
    connection.on('requestedTokens', onGetTokens);
    connection.on('requestedEndpoints', onGetEndpoints);

    connection.on('clickedNext', onClickedNext);
    connection.on('clickedBack', onClickedBack);
    connection.on('gotoStep', onGotoStep);

    function initialize (data) {
       
        if (data) {
            console.log(data)

            $.ajax({
                url: '/event/save/',
                type: 'POST',
                data: {
                    'event_id':data.eventDefinitionKey
                }
            }).done(function(result){
                console.log('saved')
            }) 

            payload = data;
        }

    }

    function onGetTokens (tokens) {
        // Response: tokens = { token: <legacy token>, fuel2token: <fuel api token> }
        console.log(tokens);
    }

    function onGetEndpoints (endpoints) {
        // Response: endpoints = { restHost: <url> } i.e. "rest.s1.qa1.exacttarget.com"
        console.log(endpoints);
    }

    function onClickedNext () {
        save();
    }

    function onClickedBack () {
        connection.trigger('prevStep');
    }

    function onGotoStep (step) {
        showStep(step);
        connection.trigger('ready');
    }

    function onRender() {
        connection.trigger('ready'); // JB will respond the first time 'ready' is called with 'initEvent'

        connection.trigger('requestTokens');
        connection.trigger('requestEndpoints');

    }

    function showStep(step, stepIndex) {
        if (stepIndex && !step) {
            step = steps[stepIndex-1];
        }

        currentStep = step;

        $('.step').hide();

        switch(currentStep.key) {
            case 'step1':
                $('#step1').show();
                break;
        }
    }

    function save() {
        payload['arguments'] = payload['arguments'] || {};
        payload['metaData'] = payload['metaData'] || {};
        payload['configurationArguments'] = payload['configurationArguments'] || {};
        payload.dataExtensionId = 'dda895e5-37bc-e611-8a02-1402ec67ad30';
        connection.trigger('updateEvent', payload);
    }
});