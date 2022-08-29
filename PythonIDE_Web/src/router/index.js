import {createRouter, createWebHashHistory} from "vue-router";

const routes=[
    {
        path:"/article",
        name:"article",
        component: () => import("../views/ArticleView.vue")
    },
    {
        path:"/user",
        name:"user",
        component: () =>import("../views/UserView.vue")
    },
];

const router = createRouter({
    history:createWebHashHistory(),
    routes
})

export default router;