import React from 'react';

const Breadcrumbs = React.lazy(() => import('./view/usage_examples/Base/Breadcrumbs'));
const Cards = React.lazy(() => import('./view/usage_examples/Base/Cards'));
const Carousels = React.lazy(() => import('./view/usage_examples/Base/Carousels'));
const Collapses = React.lazy(() => import('./view/usage_examples/Base/Collapses'));
const Dropdowns = React.lazy(() => import('./view/usage_examples/Base/Dropdowns'));
const Forms = React.lazy(() => import('./view/usage_examples/Base/Forms'));
const Jumbotrons = React.lazy(() => import('./view/usage_examples/Base/Jumbotrons'));
const ListGroups = React.lazy(() => import('./view/usage_examples/Base/ListGroups'));
const Navbars = React.lazy(() => import('./view/usage_examples/Base/Navbars'));
const Navs = React.lazy(() => import('./view/usage_examples/Base/Navs'));
const Paginations = React.lazy(() => import('./view/usage_examples/Base/Paginations'));
const Popovers = React.lazy(() => import('./view/usage_examples/Base/Popovers'));
const ProgressBar = React.lazy(() => import('./view/usage_examples/Base/ProgressBar'));
const Switches = React.lazy(() => import('./view/usage_examples/Base/Switches'));
const Tables = React.lazy(() => import('./view/usage_examples/Base/Tables'));
const Tabs = React.lazy(() => import('./view/usage_examples/Base/Tabs'));
const Tooltips = React.lazy(() => import('./view/usage_examples/Base/Tooltips'));
const BrandButtons = React.lazy(() => import('./view/usage_examples/Buttons/BrandButtons'));
const ButtonDropdowns = React.lazy(() => import('./view/usage_examples/Buttons/ButtonDropdowns'));
const ButtonGroups = React.lazy(() => import('./view/usage_examples/Buttons/ButtonGroups'));
const Buttons = React.lazy(() => import('./view/usage_examples/Buttons/Buttons'));
const Charts = React.lazy(() => import('./view/usage_examples/Charts'));
const Dashboard = React.lazy(() => import('./view/protected/pages/Dashboard'));
const CoreUIIcons = React.lazy(() => import('./view/usage_examples/Icons/CoreUIIcons'));
const Flags = React.lazy(() => import('./view/usage_examples/Icons/Flags'));
const FontAwesome = React.lazy(() => import('./view/usage_examples/Icons/FontAwesome'));
const SimpleLineIcons = React.lazy(() => import('./view/usage_examples/Icons/SimpleLineIcons'));
const Alerts = React.lazy(() => import('./view/usage_examples/Notifications/Alerts'));
const Badges = React.lazy(() => import('./view/usage_examples/Notifications/Badges'));
const Modals = React.lazy(() => import('./view/usage_examples/Notifications/Modals'));
const Colors = React.lazy(() => import('./view/usage_examples/Theme/Colors'));
const Typography = React.lazy(() => import('./view/usage_examples/Theme/Typography'));
const Widgets = React.lazy(() => import('./view/usage_examples/Widgets'));
const Users = React.lazy(() => import('./view/protected/pages/Users'));
const User = React.lazy(() => import('./view/protected/pages/Users/User'));
const Questions = React.lazy(() => import('./view/protected/pages/Questions/Questions'));
const QuestionsReorder = React.lazy(() => import('./view/protected/pages/Questions/QuestionsReorder'));
const Question = React.lazy(() => import('./view/protected/pages/Questions/Question'));
const UserGoals = React.lazy(() => import('./view/protected/pages/UserGoals/UserGoals'));
const UserGoal = React.lazy(() => import('./view/protected/pages/UserGoals/UserGoal'));
const Exercises = React.lazy(() => import('./view/protected/pages/Exercises/Exercises'));
const Exercise = React.lazy(() => import('./view/protected/pages/Exercises/Exercise'));
const ExerciseSets = React.lazy(() => import('./view/protected/pages/ExerciseSets/ExerciseSets'));
const ExerciseSet = React.lazy(() => import('./view/protected/pages/ExerciseSets/ExerciseSet'));
const ExerciseSetMappings = React.lazy(() => import('./view/protected/pages/ExerciseSetMappings/ExerciseSetMappings'));
const ExerciseSetMapping = React.lazy(() => import('./view/protected/pages/ExerciseSetMappings/ExerciseSetMapping'));
const Strategies = React.lazy(() => import('./view/protected/pages/Strategies/Strategies'));
const Strategy = React.lazy(() => import('./view/protected/pages/Strategies/Strategy'));

// https://github.com/ReactTraining/react-router/tree/master/packages/react-router-config
const routes = [
  {path: '/home/', exact: true, name: 'Home'},
  {path: '/home/dashboard', name: 'Dashboard', component: Dashboard},
  {path: '/home/theme', exact: true, name: 'Theme', component: Colors},
  {path: '/home/theme/colors', name: 'Colors', component: Colors},
  {path: '/home/theme/typography', name: 'Typography', component: Typography},
  {path: '/home/base', exact: true, name: 'Base', component: Cards},
  {path: '/home/base/cards', name: 'Cards', component: Cards},
  {path: '/home/base/forms', name: 'Forms', component: Forms},
  {path: '/home/base/switches', name: 'Switches', component: Switches},
  {path: '/home/base/tables', name: 'Tables', component: Tables},
  {path: '/home/base/tabs', name: 'Tabs', component: Tabs},
  {path: '/home/base/breadcrumbs', name: 'Breadcrumbs', component: Breadcrumbs},
  {path: '/home/base/carousels', name: 'Carousel', component: Carousels},
  {path: '/home/base/collapses', name: 'Collapse', component: Collapses},
  {path: '/home/base/dropdowns', name: 'Dropdowns', component: Dropdowns},
  {path: '/home/base/jumbotrons', name: 'Jumbotrons', component: Jumbotrons},
  {path: '/home/base/list-groups', name: 'List Groups', component: ListGroups},
  {path: '/home/base/navbars', name: 'Navbars', component: Navbars},
  {path: '/home/base/navs', name: 'Navs', component: Navs},
  {path: '/home/base/paginations', name: 'Paginations', component: Paginations},
  {path: '/home/base/popovers', name: 'Popovers', component: Popovers},
  {path: '/home/base/progress-bar', name: 'Progress Bar', component: ProgressBar},
  {path: '/home/base/tooltips', name: 'Tooltips', component: Tooltips},
  {path: '/home/buttons', exact: true, name: 'Buttons', component: Buttons},
  {path: '/home/buttons/buttons', name: 'Buttons', component: Buttons},
  {path: '/home/buttons/button-dropdowns', name: 'Button Dropdowns', component: ButtonDropdowns},
  {path: '/home/buttons/button-groups', name: 'Button Groups', component: ButtonGroups},
  {path: '/home/buttons/brand-buttons', name: 'Brand Buttons', component: BrandButtons},
  {path: '/home/icons', exact: true, name: 'Icons', component: CoreUIIcons},
  {path: '/home/icons/coreui-icons', name: 'CoreUI Icons', component: CoreUIIcons},
  {path: '/home/icons/flags', name: 'Flags', component: Flags},
  {path: '/home/icons/font-awesome', name: 'Font Awesome', component: FontAwesome},
  {path: '/home/icons/simple-line-icons', name: 'Simple Line Icons', component: SimpleLineIcons},
  {path: '/home/notifications', exact: true, name: 'Notifications', component: Alerts},
  {path: '/home/notifications/alerts', name: 'Alerts', component: Alerts},
  {path: '/home/notifications/badges', name: 'Badges', component: Badges},
  {path: '/home/notifications/modals', name: 'Modals', component: Modals},
  {path: '/home/widgets', name: 'Widgets', component: Widgets},
  {path: '/home/charts', name: 'Charts', component: Charts},
  {path: '/home/users', exact: true, name: 'Users', component: Users},
  {path: '/home/users/:id', exact: true, name: 'User Details', component: User},
  {path: '/home/modify/questions', exact: true, name: 'Questions', component: Questions},
  {path: '/home/modify/questions/order', exact: true, name: 'Question Reordering', component: QuestionsReorder},
  {path: '/home/modify/questions/:id', exact: true, name: 'Question', component: Question},
  {path: '/home/modify/user_goals', exact: true, name: 'UserGoals', component: UserGoals},
  {path: '/home/modify/user_goals/:id', exact: true, name: 'UserGoal', component: UserGoal},
  {path: '/home/modify/exercises', exact: true, name: 'Exercises', component: Exercises},
  {path: '/home/modify/exercises/:id', exact: true, name: 'Exercise', component: Exercise},
  {path: '/home/modify/exercise_sets', exact: true, name: 'ExerciseSets', component: ExerciseSets},
  {path: '/home/modify/exercise_sets/:id', exact: true, name: 'ExerciseSet', component: ExerciseSet},
  {path: '/home/modify/strategies', exact: true, name: 'Strategies', component: Strategies},
  {path: '/home/modify/strategies/:id', exact: true, name: 'Strategy', component: Strategy},
  {
    path: '/home/modify/exercise_set_mappings',
    exact: true,
    name: 'ExerciseSetMappings',
    component: ExerciseSetMappings
  },
  {
    path: '/home/modify/exercise_set_mappings/:id',
    exact: true,
    name: 'ExerciseSetMapping',
    component: ExerciseSetMapping
  },
];

export default routes;
