(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[18],{580:function(e,t,a){"use strict";a.d(t,"f",(function(){return l})),a.d(t,"m",(function(){return m})),a.d(t,"l",(function(){return d})),a.d(t,"n",(function(){return p})),a.d(t,"j",(function(){return f})),a.d(t,"g",(function(){return h})),a.d(t,"i",(function(){return v})),a.d(t,"h",(function(){return g})),a.d(t,"k",(function(){return E})),a.d(t,"t",(function(){return P})),a.d(t,"u",(function(){return k})),a.d(t,"p",(function(){return C})),a.d(t,"r",(function(){return L})),a.d(t,"q",(function(){return U})),a.d(t,"s",(function(){return I})),a.d(t,"a",(function(){return b})),a.d(t,"c",(function(){return y})),a.d(t,"b",(function(){return N})),a.d(t,"v",(function(){return T})),a.d(t,"d",(function(){return j})),a.d(t,"e",(function(){return w})),a.d(t,"o",(function(){return q}));var n=a(627),r=a.n(n),c=a(628),i=a(53),o=a(73),s=a(72),u=Object(o.a)((function e(t){var a=t.name,n=void 0===a?"":a,r=t.surname,c=void 0===r?"":r,i=t.email,o=void 0===i?"":i,u=t.role,l=void 0===u?"":u;Object(s.a)(this,e),this.name=n,this.surname=c,this.email=o,this.role=l})),l="http://".concat("localhost",":").concat("10000","/api/").concat("v1"),m="/user",d="/user/count",p="/user_goal",f="/question",h="/exercise",v="/exercise_set",g="/question_to_exercise_sets_mapping",E="/strategy",b="CREATE",y="MODIFY",N="DELETE",j="aggregateByDimension1",w="aggregateByDimension2",q="from_date";function O(e){return new Promise((function(t){return setTimeout(t,e)}))}function P(e,t){return x.apply(this,arguments)}function x(){return(x=Object(c.a)(r.a.mark((function e(t,a){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,O(1e3);case 2:if("imdavide"!==t||"xNA#6V$Eh%gZv2Pw!p2k43Eeu$XQ8&$N"!==a){e.next=7;break}return Object(i.b)("ServerApi.js","User logged in"),e.abrupt("return",new u({name:"imdavide",surname:"",email:"name.surname@localhost.com",role:"Doctor"}));case 7:if("Cov19id!@PrjDoctorPsw"!==a){e.next=12;break}return Object(i.b)("ServerApi.js","Jolly User logged in"),e.abrupt("return",new u({name:t,surname:"",email:"".concat(t,"@localhost.com"),role:"Doctor"}));case 12:return e.abrupt("return",void 0);case 13:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function k(){return S.apply(this,arguments)}function S(){return(S=Object(c.a)(r.a.mark((function e(){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:Object(i.b)("ServerApi.js","User logged out");case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function C(e){return D.apply(this,arguments)}function D(){return(D=Object(c.a)(r.a.mark((function e(t){var a,n,c,o,s,u,m,d,p,f;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=t.serverEndPoint,n=t.aggregateByDimension1,c=void 0===n?null:n,o=t.aggregateByDimension2,s=void 0===o?null:o,u=t.start,m=void 0===u?null:u,d=t.end,p=void 0===d?null:d,f=Q(f=B(f="".concat(l).concat(a,"?"),c,s),m,p),Object(i.a)("ServerApi.js","Fetching '".concat(f,"'")),e.abrupt("return",fetch(f).then((function(e){return e.json()})));case 6:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function L(e){return A.apply(this,arguments)}function A(){return(A=Object(c.a)(r.a.mark((function e(t){var a,n,c;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=t.serverEndPoint,n=t.id,c="".concat(l).concat(a,"/").concat(n),Object(i.a)("ServerApi.js","Fetching '".concat(c,"'")),e.abrupt("return",fetch(c).then((function(e){return e.json()})));case 4:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function U(e){return F.apply(this,arguments)}function F(){return(F=Object(c.a)(r.a.mark((function e(t){var a,n;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=t.serverEndPoint,n="".concat(l).concat(a),Object(i.a)("ServerApi.js","Fetching '".concat(n,"'")),e.abrupt("return",fetch(n).then((function(e){return e.json()})));case 4:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function T(e,t,a){return _.apply(this,arguments)}function _(){return(_=Object(c.a)(r.a.mark((function e(t,a,n){var c,o,s,u,m,d;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return c=n.id,o=void 0===c?null:c,s=n.formDataObject,u=void 0===s?null:s,m="".concat(l).concat(a),d={},t===b?(d.method="POST",d.body=u):t===y?(m="".concat(m,"/").concat(o),d.method="POST",d.body=u):t===N&&(m="".concat(m,"/").concat(o,"/delete"),d.method="POST"),Object(i.a)("ServerApi.js","Action: ".concat(t,", calling '").concat(m,"'")),e.abrupt("return",fetch(m,d).then((function(e){return e.json()})));case 6:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function I(e){return R.apply(this,arguments)}function R(){return(R=Object(c.a)(r.a.mark((function e(t){var a,n,c,o,s,u;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a=t.id,n=t.from_date,c=void 0===n?null:n,o=t.to_date,s=void 0===o?null:o,u=H(u="".concat(l).concat(m,"/").concat(a,"/level_history?"),c,s),Object(i.a)("ServerApi.js","Fetching '".concat(u,"'")),e.abrupt("return",fetch(u).then((function(e){return e.json()})));case 5:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function B(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;return null!==t&&(e="".concat(e,"&").concat(j,"=").concat(t)),null!==a&&(e="".concat(e,"&").concat(w,"=").concat(a)),e}function H(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;return null!==t&&(e="".concat(e,"&").concat(q,"=").concat(t)),null!==a&&(e="".concat(e,"&").concat("to_date","=").concat(a)),e}function Q(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,a=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;return null!==t&&(e="".concat(e,"&").concat("start","=").concat(t)),null!==a&&(e="".concat(e,"&").concat("end","=").concat(a)),e}},592:function(e,t,a){e.exports=a.p+"static/media/sygnet.78a4e3a4.svg"},620:function(e,t,a){},622:function(e,t,a){},623:function(e,t,a){e.exports=a.p+"static/media/data.14e3f3e2.svg"},624:function(e,t,a){e.exports=a.p+"static/media/security.de7d009e.svg"},625:function(e,t,a){e.exports=a.p+"static/media/assign.072a32a1.svg"},626:function(e,t,a){},640:function(e,t,a){"use strict";a.d(t,"c",(function(){return v})),a.d(t,"b",(function(){return b})),a.d(t,"a",(function(){return y}));var n=a(72),r=a(73),c=a(195),i=a(194),o=a(1),s=a.n(o),u=a(660),l=a(609),m=a(575),d=a(661),p=a(621),f=a(662),h=(a(620),a(109)),v=function(e){Object(c.a)(o,e);var t=Object(i.a)(o);function o(){return Object(n.a)(this,o),t.apply(this,arguments)}return Object(r.a)(o,[{key:"render",value:function(){var e=s.a.createElement(u.a,{className:"ml-auto",navbar:!0},s.a.createElement(l.a,null,s.a.createElement(h.Link,{to:"/login"},s.a.createElement(m.a,{color:"primary"},s.a.createElement("span",{className:"d-sm-none d-xs-none"},s.a.createElement("i",{className:"nc-icon nc-lock-circle-open access"})),s.a.createElement("span",{className:"d-none d-sm-block d-md-block d-lg-block d-xl-block"},"Login")))));return s.a.createElement(d.a,{color:"dark",expand:"true",className:"navbar-absolute"},s.a.createElement(p.a,{fluid:!0},s.a.createElement("div",null,s.a.createElement("img",{className:"logo-img",src:a(592),alt:"Logo"}),s.a.createElement(f.a,null,"Covid19 Project")),this.props.showNav?e:null))}}]),o}(s.a.Component),g=a(570),E=a(571),b=(a(622),function(){return s.a.createElement(p.a,null,s.a.createElement(g.a,null,s.a.createElement(E.a,null,s.a.createElement("div",{className:"logo-center"},s.a.createElement("img",{src:a(592),alt:"Covid19 Logo"})))),s.a.createElement("div",{className:"animated fadeIn"},s.a.createElement(g.a,null,s.a.createElement(E.a,{className:"land pr-0"},s.a.createElement("header",null,s.a.createElement("div",{className:"container--lg border--bottom pb3 "},s.a.createElement("h1",{className:"mb2"},"Physical activity at Covid19 time"),s.a.createElement("div",{className:"shadow-separator"}))))),s.a.createElement(g.a,null,s.a.createElement("div",{className:"info grid-wrapper"},s.a.createElement("div",null,s.a.createElement("h2",null,"Data Usage"),s.a.createElement("p",null,"Quis istud possit, inquit, negare? Videamus animi partes, quarum est conspectus illustrior; Illa sunt similia: hebes acies est cuipiam oculorum, corpore alius senescit; Non enim, si omnia non sequebatur. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem."),s.a.createElement("hr",null),s.a.createElement("p",{className:"sub"},"Ea cupidatat quis est pariatur est proident id et non officia sit velit. Ad consectetur esse do consequat."),s.a.createElement("p",{className:"cit"},"Enrico Siboni - IT Assistant @ HES-SO")),s.a.createElement("div",{className:"info-img"},s.a.createElement("img",{src:a(623),alt:"Data"}))),s.a.createElement("div",{className:"info grid-wrapper"},s.a.createElement("div",{className:"info-img"},s.a.createElement("img",{src:a(624),alt:"Security"})),s.a.createElement("div",null,s.a.createElement("h2",null,"Absolute security"),s.a.createElement("p",null,"Quis istud possit, inquit, negare? Videamus animi partes, quarum est conspectus illustrior; Illa sunt similia: hebes acies est cuipiam oculorum, corpore alius senescit; Non enim, si omnia non sequebatur. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo."),s.a.createElement("hr",null),s.a.createElement("p",{className:"sub"},"Ea id reprehenderit cupidatat incididunt labore ullamco quis qui velit ex nostrud exercitation veniam."),s.a.createElement("p",{className:"cit"},"Davide Calvaresi - PostDoctoral Researcher @ HES-SO"))),s.a.createElement("div",{className:"info grid-wrapper"},s.a.createElement("div",null,s.a.createElement("h2",null,"Research"),s.a.createElement("p",null,"Quis istud possit, inquit, negare? Videamus animi partes, quarum est conspectus illustrior; Illa sunt similia: hebes acies est cuipiam oculorum, corpore alius senescit; Non enim, si omnia non sequebatur. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem."),s.a.createElement("hr",null),s.a.createElement("p",{className:"sub"},"Labore ipsum deserunt ullamco magna. Sit velit dolor in do in in anim sint."),s.a.createElement("p",{className:"cit"},"Michael I. Schumacher - Professor @ HES-SO")),s.a.createElement("div",{className:"info-img"},s.a.createElement("img",{src:a(625),alt:"Research"}))))),s.a.createElement("div",{className:"shadow-separator"}))}),y=(a(626),function(e){Object(c.a)(a,e);var t=Object(i.a)(a);function a(){return Object(n.a)(this,a),t.apply(this,arguments)}return Object(r.a)(a,[{key:"render",value:function(){return s.a.createElement("footer",{className:"footer"+(this.props.default?" footer-default":"")},s.a.createElement(p.a,{fluid:this.props.fluid},s.a.createElement(g.a,null,s.a.createElement("nav",{className:"footer-nav"},"Covid19 Project"),s.a.createElement("div",{className:"credits ml-auto"},s.a.createElement("div",{className:"copyright"},"\xa9 ",1900+(new Date).getYear(),", made with ",s.a.createElement("i",{className:"fa fa-heart heart"})," by Enrico Siboni")))))}}]),a}(s.a.Component));a(86)},727:function(e,t,a){},889:function(e,t,a){"use strict";a.r(t);var n=a(627),r=a.n(n),c=a(628),i=a(72),o=a(73),s=a(108),u=a(195),l=a(194),m=a(1),d=a.n(m),p=a(621),f=a(570),h=a(571),v=a(728),g=a(568),E=a(569),b=a(605),y=a(629),N=a(630),j=a(588),w=a(593),q=a(575),O=a(729),P=a(744),x=a(745),k=a(640),S=a(580),C=a(53),D=(a(727),function(e){Object(u.a)(n,e);var t=Object(l.a)(n);function n(e){var a;return Object(i.a)(this,n),(a=t.call(this,e)).state={username:"",password:"",fetchingUserData:!1,forgotPasswordPopoverOpen:!1},a.toggleForgotPasswordPopover=a.toggleForgotPasswordPopover.bind(Object(s.a)(a)),a}return Object(o.a)(n,[{key:"toggleForgotPasswordPopover",value:function(){this.setState({forgotPasswordPopoverOpen:!this.state.forgotPasswordPopoverOpen})}},{key:"handleUsernameChanged",value:function(e){this.setState({username:e.target.value})}},{key:"handlePasswordChanged",value:function(e){this.setState({password:e.target.value})}},{key:"handleLoginRequest",value:function(){var e=Object(c.a)(r.a.mark((function e(t){var a;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this.setState({fetchingUserData:!0}),e.next=3,Object(S.t)(this.state.username,this.state.password);case 3:a=e.sent,this.setState({fetchingUserData:!1}),this.props.saveLoggedUser(a),Object(C.b)("Login.js","User logged in: ",a),this.props.refreshLoggedStatus();case 8:case"end":return e.stop()}}),e,this)})));return function(t){return e.apply(this,arguments)}}()},{key:"render",value:function(){var e=this;return d.a.createElement("div",{className:"app flex-row align-items-center"},d.a.createElement(p.a,null,d.a.createElement("div",{className:"fixed-top"},d.a.createElement(k.c,{showNav:!1})),d.a.createElement("div",{className:"animated fadeIn"},d.a.createElement(f.a,{className:"justify-content-center"},d.a.createElement(h.a,{md:"4"},d.a.createElement(v.a,null,d.a.createElement(g.a,{className:"p-4"},d.a.createElement(E.a,null,d.a.createElement(b.a,{onKeyPress:function(t){if("Enter"===t.key)return e.handleLoginRequest(t)}},d.a.createElement("h1",null,"Login"),d.a.createElement("p",{className:"text-muted"},"Sign In to your account"),d.a.createElement(y.a,{className:"mb-3"},d.a.createElement(N.a,{addonType:"prepend"},d.a.createElement(j.a,null,d.a.createElement("i",{className:"icon-user"}))),d.a.createElement(w.a,{type:"text",placeholder:"Username",autoComplete:"username",onChange:this.handleUsernameChanged.bind(this)})),d.a.createElement(y.a,{className:"mb-4"},d.a.createElement(N.a,{addonType:"prepend"},d.a.createElement(j.a,null,d.a.createElement("i",{className:"icon-lock"}))),d.a.createElement(w.a,{type:"password",placeholder:"Password",autoComplete:"current-password",onChange:this.handlePasswordChanged.bind(this)})),d.a.createElement(f.a,null,d.a.createElement(h.a,{xs:"6"},this.state.fetchingUserData?d.a.createElement(q.a,{color:"grey",className:"px-4",disabled:!0,onClick:this.handleLoginRequest.bind(this)},d.a.createElement("img",{className:"spinner",alt:"spinner",src:a(456)})):d.a.createElement(q.a,{color:"primary",className:"px-4",onClick:this.handleLoginRequest.bind(this)},"Login")),d.a.createElement(h.a,{xs:"6",className:"text-right"},d.a.createElement(q.a,{color:"link",className:"px-0",id:"ForgotPassword"},"Forgot password?"),d.a.createElement(O.a,{placement:"bottom",target:"ForgotPassword",isOpen:this.state.forgotPasswordPopoverOpen,toggle:this.toggleForgotPasswordPopover},d.a.createElement(P.a,null,"Help Tip!"),d.a.createElement(x.a,null,"Try to click Login anyway ",d.a.createElement("i",{className:"fa fa-smile-o fa-lg mt-4"}))))))))))))))}}]),n}(m.Component));t.default=D}}]);
//# sourceMappingURL=18.10846d6e.chunk.js.map