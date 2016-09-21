angular.module("panel-controller", [])

.controller("panelCtrl", ["$scope", "$stateParams", "$state", "contentService", "layoutService", "authenticationService", "$rootScope", function($scope, $stateParams, $state, contentService, layoutService, authenticationService, $rootScope) {
    
    var workspaceParam = $stateParams.workspace;
    var panelParam = $stateParams.panel;
	
	// data objects
    $scope.content;
	$scope.storyContent;
    $scope.geojson;
    
	// get credentials from local storage
    authenticationService.getCredentials().then(function(userData) {
        
        var user = userData;
		var objs = { multi: "panels", single: "panel" };
		var endpoint = workspaceParam + "/panels/" + user.id + "/";
		var check = { key: "url_name", value: panelParam };

		// pull panel from stored panels in service
		layoutService.getStructure(panelParam, objs, endpoint, check).then(function(panelData) {
            
            // TEMP SOLUTION PROBABLY FIXED IN REFACTOR
            // get current panel
			contentService.getData("api/panel/" + panelParam + "/").then(function(data) {

				// set scope
				$scope.content = data[0];

			});
            
            // TEMP SOLUTION PROBABLY FIXED IN REFACTOR
            contentService.getData("visualization/geojson/hexagon/").then(function(data) {
                
                // set scop
                $scope.geojson = data;
                
            });

			// get all stories for panel and persona
			contentService.getData("story/persona/" + panelData.persona_id + "/panel/" + panelData.panel_id + "/").then(function(data) {

				// set scope
				$scope.storyContent = data;

			});

		});
		
	});
    
    // country nodes
	contentService.getData("visualization/cdis/").then(function(data) {
		
		// set scope
		$scope.nodes = data;
		
	});
	
}]);