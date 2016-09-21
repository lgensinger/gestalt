angular.module("dynamic-directive-directive", [])

.directive("dynamicDirective", ["$compile", function($compile) {
	return {
		//priority: 1001,
		//terminal: true,
		restrict: 'E',
		replace: true,
		scope: {
			dir: "=",
			dirData: "=",
            dirAttributes: "="
		},
        link: function(scope, element, attrs) {
            
            // watch for directive name from api call
            scope.$watch("dir", function(newData, oldData) {
                
                // async check
                if (newData !== undefined) {
			
                    var directiveName = newData;
                    var attrs = scope.dirAttributes; console.log(attrs);

                    // add directive
                    var customDirective = angular.element("<" + directiveName + "></" + directiveName + ">");
                    
                    // check for attributes
                    if (attrs) {

                        angular.forEach(attrs, function(value, key) {

                            // check value
                            if (value.attr_value) {

                                // add attribute
                                customDirective.attr(value.attr_name, value.attr_value);

                            };

                        });

                    };

                    // add attributes
                    customDirective.attr("viz-data", "dirData");

                    // compile the custom directive
                    $compile(customDirective)(scope);

                    // add custom directive
                    element.append(customDirective);
                    
                };
                
            });
			
        }
	};
    
}]);