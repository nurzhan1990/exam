<template>
  <div>

    <div class="card mt-3" style="width: 24rem;" v-for="category in categories" :key="category.id" v-if="!question && !result">
      <div class="card-header">
        {{ category.name }}
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item" v-for="paper in category.question_papers">
          <button class="button" @click="getQuestion(paper.id)" v-if="paper.status">
            <span>{{ paper.name }}</span>
          </button>
          <button class="button" @click="getQuestion(paper.id)" v-else>
            <div><span>{{ paper.name }}</span></div>
          </button>
        </li>
      </ul>
    </div>

    <div style="width: 24rem;" v-if="question">
      <div class="card mt-3" style="width: 24rem;">
        <div class="card-header">
          {{ question.question }}
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="a" v-model="answer">
              <label class="form-check-label" for="flexCheckDefault">
                {{ question.optionA }}
              </label>
            </div>
          </li>
          <li class="list-group-item">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="b" v-model="answer">
              <label class="form-check-label" for="flexCheckDefault">
                {{ question.optionB }}
              </label>
            </div>
          </li>
          <li class="list-group-item">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="c" v-model="answer">
              <label class="form-check-label" for="flexCheckDefault">
                {{ question.optionC }}
              </label>
            </div>
          </li>
          <li class="list-group-item">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="d" v-model="answer">
              <label class="form-check-label" for="flexCheckDefault">
                {{ question.optionD }}
              </label>
            </div>
          </li>
        </ul>

      </div>
      <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-2">
        <button class="btn btn-success" type="button" @click="Answer()">Send</button>
      </div>
    </div>

    
    <div style="width: 24rem;" v-if="result">
      <div class="card mt-3" style="width: 24rem;">
        <div class="card-header">
          Результат теста
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <div class="form-check">
              <label class="form-check-label" for="flexCheckDefault">
                Всего вопросов - {{ result[0] }}, из них правильно ответили - {{ result[1] }}
              </label>
            </div>
          </li>
          <li class="list-group-item">
            <div class="form-check">
              <label class="form-check-label" for="flexCheckDefault">
                Процент правильного ответа - {{ (result[1]/result[0]*100).toFixed(2) }}
              </label>
            </div>
          </li>
        </ul>

      </div>
      <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-2">
        <button class="btn btn-success" type="button" @click="result=null, getCategories()">Exit</button>
      </div>
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
      answer: [],
      date: null,
      categories: [],
      question_papers: [],
      question: null,
      questions: [],
      active: false,
      result: null
    }
  },
  mounted() {
    this.getCategories()
  },
  methods: {
    mouseOver() {
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
    getQuestion(id) {
      this.loadState = true
      this.answer = []
      axios.get('/api/pass_exam/' + id).then(response => {
        this.question = response.data[0]
        console.log(response)
      }).catch(error => {
      })
    },
    getCsrfToken() {
      return document.cookie.match("(^|;)\\s*" + "csrftoken" + "\\s*=\\s*([^;]+)")?.pop()
    },
    Answer() {
      const headers = {
        "X-CSRFToken": this.getCsrfToken(),
        "Content-Type": "application/json",
        "Accept": "application/json",
      };
      axios.post('/api/pass_answer/', {
        answer: this.answer,
        question: this.question
      }, {headers})
      .then(response => {
        if(response.data['code'] === 200){
          this.result = response.data['res']
          this.question = null
        }else{
          this.question = response.data[0]
          this.answer = []
        }
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
