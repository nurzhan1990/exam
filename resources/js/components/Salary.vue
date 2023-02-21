<template>
  <div>

    <div class="card mt-3" style="width: 24rem;" v-for="category in categories" :key="category.id">
      <div class="card-header">
        {{ category.name }}
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="paper in category.question_papers">
          <button class="button" @click="getQuestions(paper.id)" v-if="paper.status"><div><span>{{ paper.name }}</span></div></button>
          <button class="button" @click="getQuestions(paper.id)" v-else><span>{{ paper.name }}</span></button>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
import business from 'moment-business';
import moment from 'moment';

import VueDatePicker from '@mathieustan/vue-datepicker';
import '@mathieustan/vue-datepicker/dist/vue-datepicker.min.css';

Vue.use(VueDatePicker, {
  lang: 'ru'
});
export default {
  data() {
    return {
      date: null,
      categories: [],
      question_papers: [],
      questions: [],
      active: false
    }
  },
  mounted() {
    this.getCategories()
  },
  methods: {
    mouseOver(){
        this.active = !this.active;
    },
    getCategories() {
      this.loadState = true
      axios.get('/api/categories').then(response => {
        this.categories = response.data
        console.log(response)
      }).catch(error => {
      })
    },
    getQuestPapers(id) {
      this.loadState = true
      axios.get('/api/getQuestionPaper/'+id).then(response => {
        this.question_papers = response.data
        console.log(response)
      }).catch(error => {
      })
    },
    getQuestions(id) {
      this.loadState = true
      axios.get('/api/pass_exam/'+id).then(response => {
        this.questions = response.data
        console.log(response)
      }).catch(error => {
      })
    },
  }
}
</script>

<style scoped>
.button {
  border-radius: 4px;
  background-color: #f4511e;
  border: none;
  color: #FFFFFF;
  text-align: center;
  font-size: 14px;
  padding: 20px;
  width: 335px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 5px;
}

.button span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}

.button span:after {
  content: 'Начать';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.button > div span:after {
  content: 'Продолжить';
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.button:hover span {
  padding-right: 105px;
}

.button:hover span:after {
  opacity: 1;
  right: 0;
}
</style>
