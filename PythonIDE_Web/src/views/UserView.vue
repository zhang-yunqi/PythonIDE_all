<template>
  <el-container>
    <el-header style="height: 50px;background-color: #535bf2">
      <h1>User</h1>
    </el-header>
    <el-container>
      <el-aside style="width: 300px">
        <ListOfContent @cl="select" :type="type"></ListOfContent>
      </el-aside>
      <el-main>
        <UserDetails v-if="have_item" :id="select_id"></UserDetails>
      </el-main>
    </el-container>
  </el-container>
</template>

<script  setup>
import ListOfContent from '../components/ListOfContent.vue'
import {ref} from "vue";
import {onMounted} from "vue";
import axios from "axios";
let have_item=ref(false)

onMounted(()=>{
  axios.post("http://127.0.0.1:1024/user/getname").then(function (res){
    if(res.data.usernames.length!=0){
      have_item.value=true
    }
  })
})

import UserDetails from "../components/UserDetails.vue";
let select_id = ref("0")
const type=ref("user")
function select(i){
  select_id.value=i
}

</script>