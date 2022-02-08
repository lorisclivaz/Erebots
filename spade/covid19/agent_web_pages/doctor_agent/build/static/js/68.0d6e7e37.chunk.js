(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[68],{869:function(e,t,a){},928:function(e,t,a){"use strict";a.r(t);var n=a(196),r=a(142),s=a(72),l=a(73),o=a(108),i=a(195),c=a(194),d=a(1),u=a.n(d),m=a(570),g=a(571),h=a(568),b=a(572),f=a(575),j=a(619),O=a(616),v=a(617),E=a(618),p=a(569),C=a(605),D=a(611),y=a(612),w=a(593),N=a(580),k=a(197),M=a(567),S=a(597),I=a(53),G=a(583),T=a(109),U=(a(869),function(e){Object(i.a)(d,e);var t=Object(c.a)(d);function d(e){var a,l;return Object(s.a)(this,d),(l=t.call(this,e)).userGoalData="userGoalData",l.fieldNames=[l.userGoalData],l.formID="user-goal-form",l.state=Object(r.a)(Object(r.a)({},Object(k.b)(l.fieldNames)),{},(a={objID:""},Object(n.a)(a,S.d,""),Object(n.a)(a,S.f,""),Object(n.a)(a,S.e,""),Object(n.a)(a,S.c,""),Object(n.a)(a,"uploadingChanges",!1),Object(n.a)(a,"errorMessage",""),Object(n.a)(a,"deletionModalOpen",!1),a)),l.setCurrentStateFromData.bind(Object(o.a)(l)),l.getCurrentID.bind(Object(o.a)(l)),l.handleTextChange.bind(Object(o.a)(l)),l.sendChangesToServer.bind(Object(o.a)(l)),l.setErrorMessage.bind(Object(o.a)(l)),l.toggleDeletionModal.bind(Object(o.a)(l)),l.deleteCurrentFromServer.bind(Object(o.a)(l)),l.isHandlingNewObject()||Object(k.d)(Object(o.a)(l),l.userGoalData,N.r,{serverEndPoint:N.n,id:l.getCurrentID()},(function(e){return l.setCurrentStateFromData(e)})),l}return Object(l.a)(d,[{key:"setCurrentStateFromData",value:function(e){var t;this.setState((t={objID:e[S.b][M.b]},Object(n.a)(t,S.d,e[S.d]),Object(n.a)(t,S.f,e[S.f]||""),Object(n.a)(t,S.e,e[S.e]||""),Object(n.a)(t,S.c,e[S.c]||""),t))}},{key:"getCurrentID",value:function(){return this.props.match.params.id}},{key:"isHandlingNewObject",value:function(){return"new"===this.getCurrentID()}},{key:"handleTextChange",value:function(e,t){var a={};a[e]=t,this.setState(a)}},{key:"setErrorMessage",value:function(e){this.setState({uploadingChanges:!1,errorMessage:e}),window.scrollTo(0,0)}},{key:"sendChangesToServer",value:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0];Object(I.b)("UserGoal.js","Called sendChangesToServer with insertNew=".concat(t)),this.setState({uploadingChanges:!0,errorMessage:""});var a=new FormData(document.getElementById(this.formID));if(a.get(S.d)){var n;if(t)n=Object(N.v)(N.a,N.n,{formDataObject:a});else{var r=this.getCurrentID();n=Object(N.v)(N.c,N.n,{id:r,formDataObject:a})}n.then((function(t){Object(I.a)("UserGoal.js","Saved changes to server:",t),e.setCurrentStateFromData(t),e.setState({uploadingChanges:!1}),window.history.back()}),(function(t){Object(I.c)("UserGoal.js","Error from server saving changes:",t.message),e.setErrorMessage(t.message)}))}else this.setErrorMessage("English description is mandatory!")}},{key:"toggleDeletionModal",value:function(){this.setState({deletionModalOpen:!this.state.deletionModalOpen})}},{key:"deleteCurrentFromServer",value:function(){var e=this;Object(N.v)(N.b,N.n,{id:this.getCurrentID()}).then((function(t){Object(I.a)("UserGoal.js","Deleted from server:",t),e.setState({uploadingChanges:!1}),window.history.back()}),(function(t){Object(I.c)("UserGoal.js","Error from server during deletion:",t.message),e.setErrorMessage(t.message)})),this.toggleDeletionModal()}},{key:"render",value:function(){var e=this;return u.a.createElement("div",{className:"animated fadeIn"},u.a.createElement(m.a,null,u.a.createElement(g.a,{lg:12},""===this.state.errorMessage?null:Object(k.c)(this.state.errorMessage),u.a.createElement(h.a,null,u.a.createElement(b.a,null,u.a.createElement("strong",null,u.a.createElement("i",{className:"icon-info pr-1"}),this.isHandlingNewObject()?"New User Goal":"User Goal ID: ".concat(this.state.objID)),this.isHandlingNewObject()?null:u.a.createElement(f.a,{color:"danger",onClick:this.toggleDeletionModal.bind(this),className:"mr-1 float-right"},u.a.createElement("i",{className:"fa fa-trash"})," Delete"),u.a.createElement(j.a,{isOpen:this.state.deletionModalOpen,toggle:this.toggleDeletionModal.bind(this),className:"modal-danger"},u.a.createElement(O.a,{toggle:this.toggleDeletionModal.bind(this)},"Delete User Goal"),u.a.createElement(v.a,null,"This will permanently delete the current User Goal from database.",u.a.createElement("br",null),u.a.createElement("br",null),"References to this User Goal will be removed from every data structure in which it is. This possibly includes Exercise Sets and user profiles."),u.a.createElement(E.a,null,u.a.createElement(f.a,{color:"danger",onClick:this.deleteCurrentFromServer.bind(this)},"Delete")," ",u.a.createElement(f.a,{color:"secondary",onClick:this.toggleDeletionModal.bind(this)},"Cancel")))),u.a.createElement(p.a,null,function(){var t=u.a.createElement("div",null,u.a.createElement(C.a,{id:e.formID,action:"",method:"post",encType:"multipart/form-data",className:"form-horizontal"},[S.d,S.f,S.e,S.c].map((function(t){var a=Object(G.a)(t,S.a);return u.a.createElement(D.a,{row:!0,key:t},u.a.createElement(g.a,{md:"2"},u.a.createElement(y.a,{htmlFor:"textarea-input-".concat(t)},a.keyPrettyNameLong)),u.a.createElement(g.a,{xs:"12",md:"10"},u.a.createElement(w.a,{type:"textarea",rows:"2",name:t,id:"textarea-input-".concat(t),placeholder:"".concat(a.keyPrettyNameLong," ..."),value:e.state[t],onChange:function(a){return e.handleTextChange(t,a.target.value)}})))}))),u.a.createElement("div",{className:"form-actions float-right"},u.a.createElement(f.a,{type:"submit",color:"primary",className:"mr-2",onClick:function(){return e.sendChangesToServer(e.isHandlingNewObject())},disabled:e.state.uploadingChanges},e.state.uploadingChanges?u.a.createElement("img",{className:"spinner",alt:"spinner",src:a(456)}):null,e.isHandlingNewObject()?"Insert":"Save changes"),u.a.createElement(T.Link,{to:"/home/modify/user_goals"},u.a.createElement(f.a,{color:"secondary",disabled:e.state.uploadingChanges},"Cancel"))));return e.isHandlingNewObject()?t:Object(k.f)(e,e.userGoalData,(function(e){return t}),Object(k.a)({}))}())))))}}]),d}(d.Component));t.default=U}}]);
//# sourceMappingURL=68.0d6e7e37.chunk.js.map