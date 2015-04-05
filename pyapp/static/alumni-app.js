'use strict';

var alumniapp = angular.module("dbApp", ['angularFileUpload', 'ngActivityIndicator']);


alumniapp.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
}]);


alumniapp.controller("MainController", ['$scope', 'apiFactory', '$activityIndicator',
	function($scope, dbFactory, $activityIndicator) {




	$scope.spinner = {};

	//our databases names
	$scope.databases = [];
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

	dbFactory.getDatabases()
    .success(function(data) {
    	$scope.databases = data['databases'];
    })
    .error(function(error) {
    	alert(error['message']);
    	console.log(error);
    })



	$scope.uploadDatabase = function() {

		if ($scope.files != undefined) {
			
			$activityIndicator.startAnimating();

			dbFactory.postDatabase($scope.files[0]) //multi-upload possible
			.success(function(data) {
				$activityIndicator.stopAnimating();
				$scope.databases = data['databases'];
				$scope.files = null;
			})
			.error(function(error) {
				$activityIndicator.stopAnimating();
				$scope.files = null;
				alert(error['message']);
				console.log(error);
			});
		}
		else {}
	};


	$scope.removeFile = function() {
		$scope.files = null;
	};






	$scope.reset = function() {
		$scope.workingData = {};
		$scope.showTable = false;
	};




}]); //end of MainController