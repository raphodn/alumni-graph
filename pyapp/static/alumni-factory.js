'use strict';

alumniapp.factory('apiFactory', ['$http', function($http) {
        
	var apiFactory = {};



	var apiUrlBase = '/api/';


	apiFactory.getAllData = function () {
    	return $http({
	      	url: apiUrlBase + 'all',
	      	method: 'GET'
    	});
	};


	apiFactory.postSchool = function() {

	   	return $http({
			url: apiUrlBase,
			method: 'POST',
			
   		});
	};




    return apiFactory;

}]);//end of apiFactory