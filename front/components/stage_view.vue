<template>
  <v-responsive class="overflow-y-auto mr-4" max-height="80vh" >
    <div class="d-flex justify-space-between">
      <h1>Edit Stage #{{stageData.id}}</h1>
    </div>
    <div class="d-flex flex-row align-center" style="width: 50%">
      <h3>Stage Title:</h3>
      <v-text-field v-model="stageData.title" class="ml-4"/>
<!--      <v-btn icon>-->
<!--        <v-icon large color="success">mdi-content-save</v-icon>-->
<!--      </v-btn>-->
    </div>

    <div class="ma-4">


      <v-row class="d-flex flex-column mb-2">
        <v-card>
          <v-card-title>
<!--            <v-btn icon>-->
<!--              <v-icon large color="success">mdi-content-save</v-icon>-->
<!--            </v-btn>-->
            Кнопка
          </v-card-title>
          <v-card-text>
            <v-combobox
              v-model="stageData.button"
              :items="buttons"
              label="Button choice"
              item-text="default_text"
              outlined
              dense
            ></v-combobox>
          </v-card-text>
        </v-card>
      </v-row>


      <v-row class="d-flex flex-column mb-2">
        <v-card>
          <div class="d-flex flex-row justify-space-between">
            <v-card-title>Информационные сообщения</v-card-title>
            <v-btn icon class="mt-4">
              <v-icon large>mdi-plus-circle-outline</v-icon>
            </v-btn>
          </div>
          <v-card
            v-for="(text, idx) in stageData.messages"
            :key="idx"
            color="#385F73"
            dark
            class="ma-2"
          >
            <v-card-title class="headline">
              <v-btn icon>
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              {{text.title}}
            </v-card-title>
            <v-card-subtitle style="font-size: small">{{text.default_text}}</v-card-subtitle>
          </v-card>
        </v-card>
      </v-row>


      <v-row class="d-flex flex-column mb-2">
        <v-card >
          <v-card-title>
<!--            <v-btn icon>-->
<!--              <v-icon large color="success">mdi-content-save</v-icon>-->
<!--            </v-btn>-->
            Вопрос
          </v-card-title>
<!--          {{stageData.question}}-->
          <v-card-text>
            <v-combobox
              v-model="stageData.question"
              :items="filteredTexts"
              label="Text choice"
              item-text="default_text"
              outlined
              dense
            ></v-combobox>
            <v-textarea
              v-if="stageData.question"
              v-model="stageData.question.default_text"
              dense
              auto-grow
              readonly
              row-height="0.1"
              style="font-size: 10pt;"
            >

            </v-textarea>
          </v-card-text>

        </v-card>

      </v-row>

    </div>
  </v-responsive>
</template>

<script>
    export default {
      props: {
        stageData: Object
      },
      data () {
        return {
        }
      },
      computed: {
        buttons () {
          return this.$store.getters["components/getButtons"]
        },
        texts () {
          return this.$store.getters["components/getTexts"]
        },
        filteredTexts () {
          return this.texts.filter(item => !item.is_hint)
        },
      }
    }
</script>

<style scoped>

</style>
