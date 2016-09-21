angular.module("content-service", [])

.factory("contentService", ["$http", "$q", function($http, $q) {
	
	return {
		
		// data storage
		content: "",
		
		// single http request stored in a promise
		makeRequest: function(url) {
            
            var urlBase = url.match(/api\/panel\/.+\//) ? "" : api_config.content_service_uri;
			
			// create deferred object
			var deferred = $q.defer();
			
			// make $http request
			$http.get(urlBase + url).then(function(response) {
				deferred.resolve(response.data);
			});
			
			// expose the promise data
			return deferred.promise;
			
		},
		
		// unique data requests
		getData: function(name) {
				
			var apiUrl = name;
			
			// make request
			console.log("****** GET " + apiUrl + " ******");
			this.content = this.makeRequest(apiUrl);
			
			// return stored data
			return this.content;
			
		}
		
	};
	
}]);