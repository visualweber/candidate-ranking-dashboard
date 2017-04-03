var app = angular.module('app', ['ngTagsInput']);

app.controller('main', function ($scope, $http) {
	$scope.searchSkills = [ 'java', 'html' ];
	$scope.limit = 20;

	$scope.skillTypeAhead = function (keyword) {
		return [];
	};

	$scope.candiate_matched = [];

	$scope.submit_search = function () {
		var skills = [];
		$scope.searchSkills.forEach(function (i) {
			skills.push(i.text)
		})

		skills = skills.join();

		$http.get('/api/v1/matching_candidates?skills=' + skills + '&limit=' + $scope.limit).then(function(data) {
			$scope.candiate_matched = data.data;
			console.log(data.data)
		})
	}
});