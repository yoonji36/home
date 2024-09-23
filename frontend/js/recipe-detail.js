import React from 'react';
import './recipe-detail.css';

const RecipeDetail = ({ recipe }) => {
    return (
        <div>
            <header>
                <h1>{recipe.title}</h1>
            </header>

            <main>
                <img src={recipe.image_url} alt={recipe.name} style={{ width: '300px', height: '300px' }} />
                <h2>재료</h2>
                <ul>
                    {recipe.ingredients.map((ingredient, index) => (
                        <li key={index}>{ingredient}</li>
                    ))}
                </ul>

                <h2>만드는 법</h2>
                <p>{recipe.instructions}</p>
            </main>

            <footer>
                <p>© 2024 혈당히어로 gotchA! 당뇨병 건강관리 헬스케어 웹사이트 제작</p>
                <p>all rights reserved.</p>
            </footer>
        </div>
    );
};

export default RecipeDetail;
