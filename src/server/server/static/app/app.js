var app = angular.module('taskApp', ['ngRoute', 'ngResource']);


app.config(function($locationProvider, $routeProvider) {
    // use the HTML5 History API
    $locationProvider.html5Mode(true).hashPrefix('!');

    $routeProvider
    .when('/', {
      templateUrl: 'app/views/main.html',
      controller: 'mainCtrl',
      access: {restricted: true}
    })
    .when('/home', {
      templateUrl: 'app/views/landing.html',
      controller: 'homeCtrl',
      access: {restricted: false}
    })
    .when('/logout', {
        resolve: {
            logout: function ($window, AuthService) {
                AuthService.logout(true);

                // close sidenav on mobile
                if ($window.innerWidth < 993) {
                  $('.button-collapse').sideNav('hide');
                }
            }
        }
    })
    .when('/login', {
      templateUrl: 'app/views/login.html',
      controller: 'loginCtrl',
      access: {restricted: false}
    })
    .when('/register', {
      templateUrl: 'app/views/register.html',
      controller: 'registerCtrl',
      access: {restricted: false}
    })
});

app.run(function ($rootScope, $timeout, $location, $route, ApiService, AuthService, TaskService) {

  var initial = true;

  ApiService.loadApiVersion()
  AuthService.getUserStatus()
    .then(function() {
      if (AuthService.isLoggedIn()) {
        TaskService.loadLists(false)
          .then(function(){
            // lists loaded
            initial = false;
            // initially load tasks
            TaskService.lists.forEach(function(list) {
              TaskService.loadTasks(false, list.id);
            });
          });
          // infinte spin on failure
      } else {
        initial = false;
      }
    })
    .catch(function() {
      initial = false;
    });

    // ignore files which are not dropped into the dropzone
    $('body').on('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
    });

    $('body').on('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
    });

  $timeout(function(){
    // give it some time (looks better visually)
    document.querySelector('.loading').remove();
  }, 250);


  $rootScope.$on('$routeChangeStart', function(event, next, current) {
    // Keep waiting until the userStatus was loaded
    // TODO: Implement a better solution than busy waiting
    if(initial) {
      event.preventDefault()
      $timeout(function(){
        $route.reload()
      }, 25);
    } else {
      if (next.access && next.access.restricted && AuthService.isLoggedIn() === false) {
          $location.path('/home');
      }
    }
  });

});

app.controller('rootCtrl', function($scope, $timeout, AuthService, TaskService) {

  $scope.TaskService = TaskService;
  $scope.AuthService = AuthService;

  $scope.$watch('$viewContentLoaded', function(){
    $timeout(initMaterializeComponents,0);
  });
});
