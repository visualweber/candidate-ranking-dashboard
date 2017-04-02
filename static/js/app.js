var app = angular.module('app', ['ngTagsInput']);

app.controller('main', function ($scope, $http) {
	$scope.searchSkills = [ 'java', 'html' ];

	$scope.skillTypeAhead = function (keyword) {
		return [];
	};

	$scope.candiate_matched = [
		{ candidate_id: 1, name: 'Duyet' },
		{ candidate_id: 2, name: 'Ngan' },
		{ candidate_id: 2, name: 'Ngan' },
	];
});