(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[19],{590:function(e,t,n){"use strict";n.d(t,"a",(function(){return v}));var r=n(573),o=n.n(r),a=n(576),l=n.n(a),s=n(579),i=n.n(s),c=n(581),u=n.n(c),d=n(1),p=n(586),f=n.n(p),b=n(585),h=n(589),m=function(e){function t(){for(var t,n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return t=e.call.apply(e,[this].concat(r))||this,u()(l()(t),"refHandler",(function(e){Object(h.b)(t.props.innerRef,e),Object(h.a)(t.props.setReferenceNode,e)})),t}i()(t,e);var n=t.prototype;return n.componentWillUnmount=function(){Object(h.b)(this.props.innerRef,null)},n.render=function(){return f()(Boolean(this.props.setReferenceNode),"`Reference` should not be used outside of a `Manager` component."),Object(h.c)(this.props.children)({ref:this.refHandler})},t}(d.Component);function v(e){return d.createElement(b.b.Consumer,null,(function(t){return d.createElement(m,o()({setReferenceNode:t},e))}))}},594:function(e,t,n){"use strict";var r=n(21),o=n(45),a=n(566),l=n(35),s=n(1),i=n.n(s),c=n(6),u=n.n(c),d=n(84),p=n.n(d),f=n(590),b=n(574),h=n(40),m=n(575),v={caret:u.a.bool,color:u.a.string,children:u.a.node,className:u.a.string,cssModule:u.a.object,disabled:u.a.bool,onClick:u.a.func,"aria-haspopup":u.a.bool,split:u.a.bool,tag:h.q,nav:u.a.bool},g=function(e){function t(t){var n;return(n=e.call(this,t)||this).onClick=n.onClick.bind(Object(a.a)(n)),n}Object(l.a)(t,e);var n=t.prototype;return n.onClick=function(e){this.props.disabled||this.context.disabled?e.preventDefault():(this.props.nav&&!this.props.tag&&e.preventDefault(),this.props.onClick&&this.props.onClick(e),this.context.toggle(e))},n.render=function(){var e,t=this,n=this.props,a=n.className,l=n.color,s=n.cssModule,c=n.caret,u=n.split,d=n.nav,b=n.tag,v=n.innerRef,g=Object(o.a)(n,["className","color","cssModule","caret","split","nav","tag","innerRef"]),y=g["aria-label"]||"Toggle Dropdown",O=Object(h.m)(p()(a,{"dropdown-toggle":c||u,"dropdown-toggle-split":u,"nav-link":d}),s),j=g.children||i.a.createElement("span",{className:"sr-only"},y);return d&&!b?(e="a",g.href="#"):b?e=b:(e=m.a,g.color=l,g.cssModule=s),this.context.inNavbar?i.a.createElement(e,Object(r.a)({},g,{className:O,onClick:this.onClick,"aria-expanded":this.context.isOpen,children:j})):i.a.createElement(f.a,{innerRef:v},(function(n){var o,a=n.ref;return i.a.createElement(e,Object(r.a)({},g,((o={})["string"===typeof e?"ref":"innerRef"]=a,o),{className:O,onClick:t.onClick,"aria-expanded":t.context.isOpen,children:j}))}))},t}(i.a.Component);g.propTypes=v,g.defaultProps={"aria-haspopup":!0,color:"secondary"},g.contextType=b.a,t.a=g},595:function(e,t,n){"use strict";var r=n(21),o=n(74),a=n(45),l=n(35),s=n(1),i=n.n(s),c=n(6),u=n.n(c),d=n(84),p=n.n(d),f=n(666),b=n(574),h=n(40),m={tag:h.q,children:u.a.node.isRequired,right:u.a.bool,flip:u.a.bool,modifiers:u.a.object,className:u.a.string,cssModule:u.a.object,persist:u.a.bool,positionFixed:u.a.bool},v={flip:{enabled:!1}},g={up:"top",left:"left",right:"right",down:"bottom"},y=function(e){function t(){return e.apply(this,arguments)||this}return Object(l.a)(t,e),t.prototype.render=function(){var e=this,t=this.props,n=t.className,l=t.cssModule,s=t.right,c=t.tag,u=t.flip,d=t.modifiers,b=t.persist,m=t.positionFixed,y=Object(a.a)(t,["className","cssModule","right","tag","flip","modifiers","persist","positionFixed"]),O=Object(h.m)(p()(n,"dropdown-menu",{"dropdown-menu-right":s,show:this.context.isOpen}),l),j=c;if(b||this.context.isOpen&&!this.context.inNavbar){var E=(g[this.context.direction]||"bottom")+"-"+(s?"end":"start"),C=u?d:Object(o.a)({},d,{},v),N=!!m;return i.a.createElement(f.a,{placement:E,modifiers:C,positionFixed:N},(function(t){var n=t.ref,o=t.style,a=t.placement;return i.a.createElement(j,Object(r.a)({tabIndex:"-1",role:"menu",ref:n,style:o},y,{"aria-hidden":!e.context.isOpen,className:O,"x-placement":a}))}))}return i.a.createElement(j,Object(r.a)({tabIndex:"-1",role:"menu"},y,{"aria-hidden":!this.context.isOpen,className:O,"x-placement":y.placement}))},t}(i.a.Component);y.propTypes=m,y.defaultProps={tag:"div",flip:!0},y.contextType=b.a,t.a=y},596:function(e,t,n){"use strict";var r=n(21),o=n(45),a=n(566),l=n(35),s=n(1),i=n.n(s),c=n(6),u=n.n(c),d=n(84),p=n.n(d),f=n(574),b=n(40),h={children:u.a.node,active:u.a.bool,disabled:u.a.bool,divider:u.a.bool,tag:b.q,header:u.a.bool,onClick:u.a.func,className:u.a.string,cssModule:u.a.object,toggle:u.a.bool},m=function(e){function t(t){var n;return(n=e.call(this,t)||this).onClick=n.onClick.bind(Object(a.a)(n)),n.getTabIndex=n.getTabIndex.bind(Object(a.a)(n)),n}Object(l.a)(t,e);var n=t.prototype;return n.onClick=function(e){this.props.disabled||this.props.header||this.props.divider?e.preventDefault():(this.props.onClick&&this.props.onClick(e),this.props.toggle&&this.context.toggle(e))},n.getTabIndex=function(){return this.props.disabled||this.props.header||this.props.divider?"-1":"0"},n.render=function(){var e=this.getTabIndex(),t=e>-1?"menuitem":void 0,n=Object(b.n)(this.props,["toggle"]),a=n.className,l=n.cssModule,s=n.divider,c=n.tag,u=n.header,d=n.active,f=Object(o.a)(n,["className","cssModule","divider","tag","header","active"]),h=Object(b.m)(p()(a,{disabled:f.disabled,"dropdown-item":!s&&!u,active:d,"dropdown-header":u,"dropdown-divider":s}),l);return"button"===c&&(u?c="h6":s?c="div":f.href&&(c="a")),i.a.createElement(c,Object(r.a)({type:"button"===c&&(f.onClick||this.props.toggle)?"button":void 0},f,{tabIndex:e,role:t,className:h,onClick:this.onClick}))},t}(i.a.Component);m.propTypes=h,m.defaultProps={tag:"button",toggle:!0},m.contextType=f.a,t.a=m},609:function(e,t,n){"use strict";var r=n(21),o=n(45),a=n(1),l=n.n(a),s=n(6),i=n.n(s),c=n(84),u=n.n(c),d=n(40),p={tag:d.q,"aria-label":i.a.string,className:i.a.string,cssModule:i.a.object,role:i.a.string,size:i.a.string,vertical:i.a.bool},f=function(e){var t=e.className,n=e.cssModule,a=e.size,s=e.vertical,i=e.tag,c=Object(o.a)(e,["className","cssModule","size","vertical","tag"]),p=Object(d.m)(u()(t,!!a&&"btn-group-"+a,s?"btn-group-vertical":"btn-group"),n);return l.a.createElement(i,Object(r.a)({},c,{className:p}))};f.propTypes=p,f.defaultProps={tag:"div",role:"group"},t.a=f},632:function(e,t,n){"use strict";var r=n(21),o=n(1),a=n.n(o),l=n(6),s=n.n(l),i=n(604),c={children:s.a.node},u=function(e){return a.a.createElement(i.a,Object(r.a)({group:!0},e))};u.propTypes=c,t.a=u},635:function(e,t,n){!function(e){"use strict";function t(e){var t=this,n="above",r="below",o="chartjs-tooltip",a="no-transform",l="tooltip-body",s="tooltip-body-item",i="tooltip-body-item-color",c="tooltip-body-item-label",u="tooltip-body-item-value",d="tooltip-header",p="tooltip-header-item",f={DIV:"div",SPAN:"span",TOOLTIP:(this._chart.canvas.id||function(){var e=function(){return(65536*(1+Math.random())|0).toString(16)},n="_canvas-"+(e()+e());return t._chart.canvas.id=n,n}())+"-tooltip"},b=document.getElementById(f.TOOLTIP);if(b||((b=document.createElement("div")).id=f.TOOLTIP,b.className=o,this._chart.canvas.parentNode.appendChild(b)),0!==e.opacity){if(b.classList.remove(n,r,a),e.yAlign?b.classList.add(e.yAlign):b.classList.add(a),e.body){var h=e.title||[],m=document.createElement(f.DIV);m.className=d,h.forEach((function(e){var t=document.createElement(f.DIV);t.className=p,t.innerHTML=e,m.appendChild(t)}));var v=document.createElement(f.DIV);v.className=l,e.body.map((function(e){return e.lines})).forEach((function(t,n){var r=document.createElement(f.DIV);r.className=s;var o=e.labelColors[n],a=document.createElement(f.SPAN);if(a.className=i,a.style.backgroundColor=o.backgroundColor,r.appendChild(a),t[0].split(":").length>1){var l=document.createElement(f.SPAN);l.className=c,l.innerHTML=t[0].split(": ")[0],r.appendChild(l);var d=document.createElement(f.SPAN);d.className=u,d.innerHTML=t[0].split(": ").pop(),r.appendChild(d)}else{var p=document.createElement(f.SPAN);p.className=u,p.innerHTML=t[0],r.appendChild(p)}v.appendChild(r)})),b.innerHTML="",b.appendChild(m),b.appendChild(v)}var g=this._chart.canvas.getBoundingClientRect(),y=this._chart.canvas.offsetTop,O=this._chart.canvas.offsetLeft+e.caretX,j=y+e.caretY,E=e.width/2;O+E>g.width?O-=E:O<E&&(O+=E),b.style.opacity=1,b.style.left=O+"px",b.style.top=j+"px"}else b.style.opacity=0}var n=t;e.CustomTooltips=t,e.customTooltips=n,Object.defineProperty(e,"__esModule",{value:!0})}(t)},650:function(e,t,n){"use strict";function r(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}n.d(t,"a",(function(){return r}))},678:function(e,t,n){"use strict";n.d(t,"a",(function(){return o}));var r=n(650);function o(e,t){if(e){if("string"===typeof e)return Object(r.a)(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(n):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Object(r.a)(e,t):void 0}}},681:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),o=n(1),a=i(o),l=i(n(6)),s=i(n(682));function i(e){return e&&e.__esModule?e:{default:e}}var c=function(e){function t(e){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t);var n=function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!==typeof t&&"function"!==typeof t?e:t}(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,e));return n.detectFullScreen=n.detectFullScreen.bind(n),n}return function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),r(t,[{key:"componentDidMount",value:function(){s.default.addEventListener("fullscreenchange",this.detectFullScreen)}},{key:"componentWillUnmount",value:function(){s.default.removeEventListener("fullscreenchange",this.detectFullScreen)}},{key:"componentDidUpdate",value:function(){this.handleProps(this.props)}},{key:"handleProps",value:function(e){var t=s.default.fullscreenElement===this.node;t&&!e.enabled?this.leaveFullScreen():!t&&e.enabled&&this.enterFullScreen()}},{key:"detectFullScreen",value:function(){this.props.onChange&&this.props.onChange(s.default.fullscreenElement===this.node)}},{key:"enterFullScreen",value:function(){s.default.fullscreenEnabled&&s.default.requestFullscreen(this.node)}},{key:"leaveFullScreen",value:function(){s.default.fullscreenEnabled&&s.default.exitFullscreen()}},{key:"render",value:function(){var e=this,t=["fullscreen"];return this.props.enabled&&t.push("fullscreen-enabled"),a.default.createElement("div",{className:t.join(" "),ref:function(t){return e.node=t},style:this.props.enabled?{height:"100%",width:"100%"}:void 0},this.props.children)}}]),t}(o.Component);c.propTypes={children:l.default.node.isRequired,enabled:l.default.bool.isRequired,onChange:l.default.func},c.defaultProps={enabled:!1},t.default=c},682:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r={fullscreenEnabled:0,fullscreenElement:1,requestFullscreen:2,exitFullscreen:3,fullscreenchange:4,fullscreenerror:5},o=["webkitFullscreenEnabled","webkitFullscreenElement","webkitRequestFullscreen","webkitExitFullscreen","webkitfullscreenchange","webkitfullscreenerror"],a=["mozFullScreenEnabled","mozFullScreenElement","mozRequestFullScreen","mozCancelFullScreen","mozfullscreenchange","mozfullscreenerror"],l=["msFullscreenEnabled","msFullscreenElement","msRequestFullscreen","msExitFullscreen","MSFullscreenChange","MSFullscreenError"],s="undefined"!==typeof window&&"undefined"!==typeof window.document?window.document:{},i="fullscreenEnabled"in s&&Object.keys(r)||o[0]in s&&o||a[0]in s&&a||l[0]in s&&l||[];t.default={requestFullscreen:function(e){return e[i[r.requestFullscreen]]()},requestFullscreenFunction:function(e){return e[i[r.requestFullscreen]]},get exitFullscreen(){return s[i[r.exitFullscreen]].bind(s)},addEventListener:function(e,t,n){return s.addEventListener(i[r[e]],t,n)},removeEventListener:function(e,t,n){return s.removeEventListener(i[r[e]],t,n)},get fullscreenEnabled(){return Boolean(s[i[r.fullscreenEnabled]])},set fullscreenEnabled(e){},get fullscreenElement(){return s[i[r.fullscreenElement]]},set fullscreenElement(e){},get onfullscreenchange(){return s[("on"+i[r.fullscreenchange]).toLowerCase()]},set onfullscreenchange(e){return s[("on"+i[r.fullscreenchange]).toLowerCase()]=e},get onfullscreenerror(){return s[("on"+i[r.fullscreenerror]).toLowerCase()]},set onfullscreenerror(e){return s[("on"+i[r.fullscreenerror]).toLowerCase()]=e}}},700:function(e,t,n){"use strict";var r=n(21),o=n(45),a=n(1),l=n.n(a),s=n(6),i=n.n(s),c=n(84),u=n.n(c),d=n(40),p={className:i.a.string,cssModule:i.a.object,size:i.a.string,bordered:i.a.bool,borderless:i.a.bool,striped:i.a.bool,dark:i.a.bool,hover:i.a.bool,responsive:i.a.oneOfType([i.a.bool,i.a.string]),tag:d.q,responsiveTag:d.q,innerRef:i.a.oneOfType([i.a.func,i.a.string,i.a.object])},f=function(e){var t=e.className,n=e.cssModule,a=e.size,s=e.bordered,i=e.borderless,c=e.striped,p=e.dark,f=e.hover,b=e.responsive,h=e.tag,m=e.responsiveTag,v=e.innerRef,g=Object(o.a)(e,["className","cssModule","size","bordered","borderless","striped","dark","hover","responsive","tag","responsiveTag","innerRef"]),y=Object(d.m)(u()(t,"table",!!a&&"table-"+a,!!s&&"table-bordered",!!i&&"table-borderless",!!c&&"table-striped",!!p&&"table-dark",!!f&&"table-hover"),n),O=l.a.createElement(h,Object(r.a)({},g,{ref:v,className:y}));if(b){var j=Object(d.m)(!0===b?"table-responsive":"table-responsive-"+b,n);return l.a.createElement(m,{className:j},O)}return O};f.propTypes=p,f.defaultProps={tag:"table",responsiveTag:"div"},t.a=f},701:function(e,t,n){"use strict";var r=n(21),o=n(45),a=n(1),l=n.n(a),s=n(6),i=n.n(s),c=n(84),u=n.n(c),d=n(40),p={tag:d.q,"aria-label":i.a.string,className:i.a.string,cssModule:i.a.object,role:i.a.string},f=function(e){var t=e.className,n=e.cssModule,a=e.tag,s=Object(o.a)(e,["className","cssModule","tag"]),i=Object(d.m)(u()(t,"btn-toolbar"),n);return l.a.createElement(a,Object(r.a)({},s,{className:i}))};f.propTypes=p,f.defaultProps={tag:"div",role:"toolbar"},t.a=f},883:function(e,t,n){"use strict";n.d(t,"a",(function(){return o}));var r=n(678);function o(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if("undefined"!==typeof Symbol&&Symbol.iterator in Object(e)){var n=[],r=!0,o=!1,a=void 0;try{for(var l,s=e[Symbol.iterator]();!(r=(l=s.next()).done)&&(n.push(l.value),!t||n.length!==t);r=!0);}catch(i){o=!0,a=i}finally{try{r||null==s.return||s.return()}finally{if(o)throw a}}return n}}(e,t)||Object(r.a)(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}}}]);
//# sourceMappingURL=19.a19a8565.chunk.js.map