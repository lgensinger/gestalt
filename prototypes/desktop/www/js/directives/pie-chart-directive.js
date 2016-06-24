angular.module("pie-chart-directive", [])

.directive("pieChart", ["plotlyService", function(plotlyService) {
	return {
		restrict: "E",
		scope: {
			vizData: "="
		},
		template: "<div style='width: 500px; height: 500px;'></div>",
		link: function(scope, element, attrs) {
			
			// get plotly promise
			plotlyService.Plotly().then(function(Plotly) {
                
                var canvas = element.find("div")[0];
                
                // bind data
                scope.$watch("vizData", function(newData, oldData) {
                	
                    // async check
                    if (newData !== undefined) {
                        
                        function draw(data) {
                            
                            ////////////////////////////////////////
                            /////////// START PLOTLY CODE ///////////
                            /////////////////////////////////////////
                            
                            // get chart metadata
                            var plotDefs = getPlot(data);

                            // plot chart in canvas
                            Plotly.newPlot(canvas, plotDefs.viz, plotDefs.layout, plotDefs.configs);

                            function getPlot(data) {

                                // data to plot
                                var viz = [{
                                    values: data,
                                    labels: ["bugs", "enhancements"],
                                    domain: {
                                        x: [0, .48]
                                    },
                                    hole: .7,
                                    hoverinfo: "label",
                                    type: "pie"
                                }];

                                // layout for plot
                                var layout = {
                                    height: 500,
                                    width: 500
                                };

                                // configs for plot
                                var plotConfigs = {
                                    showLink: false
                                };

                                return { viz: viz, layout: layout, configs: plotConfigs };

                            };
                            
                            ////////////////////////////////////////
                            /////////// END PLOTLY CODE ///////////
                            /////////////////////////////////////////

                        };
                        
                        draw(newData);
                        
                    };
                    
                });
				
			});
			
		}
		
	};
}]);