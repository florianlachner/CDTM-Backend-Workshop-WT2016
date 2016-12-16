app.controller('mainCtrl', function($scope, $interval, $timeout, AuthService, TaskService) {

  // TODO: find a better solution to busy waiting
  var reloadTasks = $interval(function() {
    if (AuthService.isLoggedIn()) {
      TaskService.lists.forEach(function(list) {
        TaskService.loadTasks(false, list.id);
      });
    } else {
      $interval.cancel(reloadTasks);
    }
  }, 10000);

});
