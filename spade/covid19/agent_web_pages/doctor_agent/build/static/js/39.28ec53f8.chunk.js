(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[39],{573:function(e,t){function n(){return e.exports=n=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(e[o]=n[o])}return e},e.exports.__esModule=!0,e.exports.default=e.exports,n.apply(this,arguments)}e.exports=n,e.exports.__esModule=!0,e.exports.default=e.exports},577:function(e,t,n){"use strict";var o=n(455);t.__esModule=!0,t.getScrollbarWidth=i,t.setScrollbarWidth=l,t.isBodyOverflowing=c,t.getOriginalBodyPadding=function(){var e=window.getComputedStyle(document.body,null);return parseInt(e&&e.getPropertyValue("padding-right")||0,10)},t.conditionallyUpdateScrollbar=function(){var e=i(),t=document.querySelectorAll(".fixed-top, .fixed-bottom, .is-fixed, .sticky-top")[0],n=t?parseInt(t.style.paddingRight||0,10):0;c()&&l(n+e)},t.setGlobalCssModule=function(e){r=e},t.mapToCssModules=function(e,t){void 0===e&&(e="");void 0===t&&(t=r);return t?e.split(" ").map((function(e){return t[e]||e})).join(" "):e},t.omit=function(e,t){var n={};return Object.keys(e).forEach((function(o){-1===t.indexOf(o)&&(n[o]=e[o])})),n},t.pick=function(e,t){var n,o=Array.isArray(t)?t:[t],r=o.length,a={};for(;r>0;)n=o[r-=1],a[n]=e[n];return a},t.warnOnce=u,t.deprecated=function(e,t){return function(n,o,r){null!==n[o]&&"undefined"!==typeof n[o]&&u('"'+o+'" property of "'+r+'" has been deprecated.\n'+t);for(var a=arguments.length,i=new Array(a>3?a-3:0),l=3;l<a;l++)i[l-3]=arguments[l];return e.apply(void 0,[n,o,r].concat(i))}},t.DOMElement=f,t.isReactRefObj=y,t.toNumber=function(e){var t=typeof e;if("number"===t)return e;if("symbol"===t||"object"===t&&"[object Symbol]"===g(e))return NaN;if(v(e)){var n="function"===typeof e.valueOf?e.valueOf():e;e=v(n)?""+n:n}if("string"!==t)return 0===e?e:+e;e=e.replace(/^\s+|\s+$/g,"");var o=/^0b[01]+$/i.test(e);return o||/^0o[0-7]+$/i.test(e)?parseInt(e.slice(2),o?2:8):/^[-+]0x[0-9a-f]+$/i.test(e)?NaN:+e},t.isObject=v,t.isFunction=h,t.findDOMElements=E,t.isArrayOrNodeList=O,t.getTarget=function(e,t){var n=E(e);return t?O(n)?n:null===n?[]:[n]:O(n)?n[0]:n},t.addMultipleEventListeners=function(e,t,n,o){var r=e;O(r)||(r=[r]);var a=n;"string"===typeof a&&(a=a.split(/\s+/));if(!O(r)||"function"!==typeof t||!Array.isArray(a))throw new Error("\n      The first argument of this function must be DOM node or an array on DOM nodes or NodeList.\n      The second must be a function.\n      The third is a string or an array of strings that represents DOM events\n    ");return Array.prototype.forEach.call(a,(function(e){Array.prototype.forEach.call(r,(function(n){n.addEventListener(e,t,o)}))})),function(){Array.prototype.forEach.call(a,(function(e){Array.prototype.forEach.call(r,(function(n){n.removeEventListener(e,t,o)}))}))}},t.focusableElements=t.defaultToggleEvents=t.canUseDOM=t.PopperPlacements=t.keyCodes=t.TransitionStatuses=t.TransitionPropTypeKeys=t.TransitionTimeouts=t.tagPropType=t.targetPropType=void 0;var r,a=o(n(6));function i(){var e=document.createElement("div");e.style.position="absolute",e.style.top="-9999px",e.style.width="50px",e.style.height="50px",e.style.overflow="scroll",document.body.appendChild(e);var t=e.offsetWidth-e.clientWidth;return document.body.removeChild(e),t}function l(e){document.body.style.paddingRight=e>0?e+"px":null}function c(){return document.body.clientWidth<window.innerWidth}var s={};function u(e){s[e]||("undefined"!==typeof console&&console.error(e),s[e]=!0)}var d="object"===typeof window&&window.Element||function(){};function f(e,t,n){if(!(e[t]instanceof d))return new Error("Invalid prop `"+t+"` supplied to `"+n+"`. Expected prop to be an instance of Element. Validation failed.")}var p=a.default.oneOfType([a.default.string,a.default.func,f,a.default.shape({current:a.default.any})]);t.targetPropType=p;var b=a.default.oneOfType([a.default.func,a.default.string,a.default.shape({$$typeof:a.default.symbol,render:a.default.func}),a.default.arrayOf(a.default.oneOfType([a.default.func,a.default.string,a.default.shape({$$typeof:a.default.symbol,render:a.default.func})]))]);t.tagPropType=b;t.TransitionTimeouts={Fade:150,Collapse:350,Modal:300,Carousel:600};t.TransitionPropTypeKeys=["in","mountOnEnter","unmountOnExit","appear","enter","exit","timeout","onEnter","onEntering","onEntered","onExit","onExiting","onExited"];t.TransitionStatuses={ENTERING:"entering",ENTERED:"entered",EXITING:"exiting",EXITED:"exited"};t.keyCodes={esc:27,space:32,enter:13,tab:9,up:38,down:40,home:36,end:35,n:78,p:80};t.PopperPlacements=["auto-start","auto","auto-end","top-start","top","top-end","right-start","right","right-end","bottom-end","bottom","bottom-start","left-end","left","left-start"];var m=!("undefined"===typeof window||!window.document||!window.document.createElement);function y(e){return!(!e||"object"!==typeof e)&&"current"in e}function g(e){return null==e?void 0===e?"[object Undefined]":"[object Null]":Object.prototype.toString.call(e)}function v(e){var t=typeof e;return null!=e&&("object"===t||"function"===t)}function h(e){if(!v(e))return!1;var t=g(e);return"[object Function]"===t||"[object AsyncFunction]"===t||"[object GeneratorFunction]"===t||"[object Proxy]"===t}function E(e){if(y(e))return e.current;if(h(e))return e();if("string"===typeof e&&m){var t=document.querySelectorAll(e);if(t.length||(t=document.querySelectorAll("#"+e)),!t.length)throw new Error("The target '"+e+"' could not be identified in the dom, tip: check spelling");return t}return e}function O(e){return null!==e&&(Array.isArray(e)||m&&"number"===typeof e.length)}t.canUseDOM=m;t.defaultToggleEvents=["touchstart","click"];t.focusableElements=["a[href]","area[href]","input:not([disabled]):not([type=hidden])","select:not([disabled])","textarea:not([disabled])","button:not([disabled])","object","embed","[tabindex]:not(.modal)","audio[controls]","video[controls]",'[contenteditable]:not([contenteditable="false"])']},582:function(e,t){e.exports=function(e,t){if(null==e)return{};var n,o,r={},a=Object.keys(e);for(o=0;o<a.length;o++)n=a[o],t.indexOf(n)>=0||(r[n]=e[n]);return r},e.exports.__esModule=!0,e.exports.default=e.exports},603:function(e,t,n){"use strict";var o=n(455);t.__esModule=!0,t.default=void 0;var r=o(n(573)),a=o(n(582)),i=o(n(576)),l=o(n(579)),c=o(n(1)),s=o(n(6)),u=o(n(84)),d=n(577),f={active:s.default.bool,"aria-label":s.default.string,block:s.default.bool,color:s.default.string,disabled:s.default.bool,outline:s.default.bool,tag:d.tagPropType,innerRef:s.default.oneOfType([s.default.object,s.default.func,s.default.string]),onClick:s.default.func,size:s.default.string,children:s.default.node,className:s.default.string,cssModule:s.default.object,close:s.default.bool},p=function(e){function t(t){var n;return(n=e.call(this,t)||this).onClick=n.onClick.bind((0,i.default)(n)),n}(0,l.default)(t,e);var n=t.prototype;return n.onClick=function(e){this.props.disabled?e.preventDefault():this.props.onClick&&this.props.onClick(e)},n.render=function(){var e=this.props,t=e.active,n=e["aria-label"],o=e.block,i=e.className,l=e.close,s=e.cssModule,f=e.color,p=e.outline,b=e.size,m=e.tag,y=e.innerRef,g=(0,a.default)(e,["active","aria-label","block","className","close","cssModule","color","outline","size","tag","innerRef"]);l&&"undefined"===typeof g.children&&(g.children=c.default.createElement("span",{"aria-hidden":!0},"\xd7"));var v="btn"+(p?"-outline":"")+"-"+f,h=(0,d.mapToCssModules)((0,u.default)(i,{close:l},l||"btn",l||v,!!b&&"btn-"+b,!!o&&"btn-block",{active:t,disabled:this.props.disabled}),s);g.href&&"button"===m&&(m="a");var E=l?"Close":null;return c.default.createElement(m,(0,r.default)({type:"button"===m&&g.onClick?"button":void 0},g,{className:h,ref:y,onClick:this.onClick,"aria-label":n||E}))},t}(c.default.Component);p.propTypes=f,p.defaultProps={color:"secondary",tag:"button"};var b=p;t.default=b},639:function(e,t,n){"use strict";var o=n(455);t.__esModule=!0,t.default=void 0;var r=o(n(573)),a=o(n(582)),i=o(n(1)),l=o(n(6)),c=o(n(84)),s=n(577),u={tag:s.tagPropType,top:l.default.bool,bottom:l.default.bool,className:l.default.string,cssModule:l.default.object},d=function(e){var t=e.className,n=e.cssModule,o=e.top,l=e.bottom,u=e.tag,d=(0,a.default)(e,["className","cssModule","top","bottom","tag"]),f="card-img";o&&(f="card-img-top"),l&&(f="card-img-bottom");var p=(0,s.mapToCssModules)((0,c.default)(t,f),n);return i.default.createElement(u,(0,r.default)({},d,{className:p}))};d.propTypes=u,d.defaultProps={tag:"img"};var f=d;t.default=f},870:function(e,t,n){},929:function(e,t,n){"use strict";n.r(t);var o=n(142),r=n(72),a=n(73),i=n(195),l=n(194),c=n(1),s=n.n(c),u=n(570),d=n(571),f=n(568),p=n(572),b=n(569),m=n(580),y=n(197),g=n(606),v=n.n(g),h=(n(870),n(567)),E=n(583),O=n(587),x=n(603),j=n.n(x),w=n(109),T=n(639),k=n.n(T),N=function(e){return"/home/modify/exercises/".concat(e)},M=function(e){Object(i.a)(n,e);var t=Object(l.a)(n);function n(e){var a;return Object(r.a)(this,n),(a=t.call(this,e)).allExercisesField="allExercises",a.fieldNames=[a.allExercisesField],a.state=Object(o.a)({},Object(y.b)(a.fieldNames)),a}return Object(a.a)(n,[{key:"componentDidMount",value:function(){Object(y.d)(this,this.allExercisesField,m.p,{serverEndPoint:m.g})}},{key:"render",value:function(){return s.a.createElement("div",{className:"animated fadeIn"},s.a.createElement(u.a,null,s.a.createElement(d.a,{xl:12},s.a.createElement(f.a,null,s.a.createElement(p.a,null,s.a.createElement("i",{className:"fa fa-align-justify"})," Exercises",s.a.createElement("div",{className:"card-header-actions"},s.a.createElement(w.Link,{to:N("new")},s.a.createElement(j.a,{size:"sm",color:"success"},s.a.createElement("i",{className:"fa fa-plus"})," New")))),s.a.createElement(b.a,null,Object(y.f)(this,this.allExercisesField,(function(e){var t="Actions",n="GIF Image",o="User Shown Description",r=[O.c,o,n,t],a=r.map((function(e){var r,a={name:Object(E.b)(e,!1,O.a),sortable:!0,grow:(r=e,[o].includes(r)?"8":[].includes(r)?"6":[t,n].includes(r)?"1":"4"),center:[n,t].includes(e),wrap:[o,O.c].includes(e),selector:function(r){return[n,t].includes(e)?"":e===o?r[O.e]:Object(E.a)(e,O.a).valuePrettifier(r[e],!0,!1)},format:function(r){if(e===t)return s.a.createElement(w.Link,{to:N(r[O.b][h.b])},s.a.createElement(j.a,{color:"primary",size:"sm",outline:!0},s.a.createElement("i",{className:"cui-pencil icons font-1xl d-block"})));if(e===o)return r[O.e];if(e===n){var a=r[O.b][h.b];return s.a.createElement(k.a,{id:a,alt:"Exercise Image preview",key:a,src:"".concat(m.f).concat(m.g,"/").concat(a,"/gif?random=").concat(performance.now())})}return Object(E.a)(e,O.a).valuePrettifier(r[e],!0,!0)}},i=function(e){return[].includes(e)?"lg":[n,O.c].includes(e)?"md":[].includes(e)?"sm":null}(e);return null!=i&&(a.hide=i),a}));return s.a.createElement(v.a,{noHeader:!0,columns:a,data:e,keyField:"".concat(O.b,".").concat(h.b),striped:!0,highlightOnHover:!0,noDataComponent:Object(y.e)(),dense:!0,pagination:!0,paginationPerPage:50,paginationRowsPerPageOptions:[5,10,20,50,100,200,500],className:"exercises-table"})}),Object(y.a)({})))))))}}]),n}(c.Component);t.default=M}}]);
//# sourceMappingURL=39.28ec53f8.chunk.js.map