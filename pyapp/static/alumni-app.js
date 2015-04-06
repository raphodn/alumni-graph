'use strict';

var alumniapp = angular.module("alumniApp", ['angularFileUpload', 'ngActivityIndicator']);


alumniapp.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
}]);


alumniapp.controller("MainController", ['$scope', 'apiFactory', '$activityIndicator',
	function($scope, apiFactory, $activityIndicator) {




	$scope.tab = {};
	$scope.tab.value = 1;

	//our databases names
	$scope.all_nodes;
	$scope.all_rels;
	//object we are working on
	$scope.workingData = {};
	// tables of the database we are working on
	$scope.working_database_tables = null;
	//columns of the table of the database we are working on
	$scope.working_database_table_columns = null;
	//show final table
	$scope.showTable = false;

	
	/*
	 * initialization
	 * Get existing database files in the database folder
	 *
	*/

	$activityIndicator.startAnimating();

	apiFactory.getAllData()
    .success(function(data) {
    	$activityIndicator.stopAnimating();
    	console.log(data);
    	$scope.all_nodes = data['nodes'];
    	$scope.all_rels = data['relationships'];
    })
    .error(function(error) {
    	$activityIndicator.stopAnimating();
    	alert(error['message']);
    	console.log(error);
    })







}]); //end of MainController